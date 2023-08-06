# encoding: utf8
"""Load and validate a python module received as a filename.

"""
import os
import re
import glob
import json
import inspect
import textwrap
import importlib
import itertools
import traceback
from functools import partial
from collections import namedtuple, defaultdict

import clyngor
from biseau import utils


DEFAULT_DOC = 'NO SCRIPT DOC PROVIDED. Fix this by writing a module documentation inside script definition.'
RETURNS_TYPES = {iter, str}
OPTIONS_TYPES = {int, float, bool, str, list, open, partial}
TYPE_DEFAULT = {int: 0, float: 0., bool: False, str: '', list: (), open: None, partial: None}
REGEX_OPTION_DESC = re.compile(r'([a-zA-Z0-9_]+)\s*--\s*(.+)$')

class ScriptError(ValueError):
    pass


Script = namedtuple('Script', 'name, tags, description, module, run_on, options, input_mode, incompatible, active_by_default, spec_inputs, spec_outputs, inputs, outputs, source_view, disabled, erase_context')
# name -- human readable name
# tags -- set of tags identifying the script
# description -- human readable and high level description of the script
# module -- reference to the module itself
# run_on -- function in module to call on context
# options -- list of (name, type, default, description) describing each option
# input_mode -- define if run_on must receive the context or the resulting ASP models
# incompatible -- list of incompatibles modules
# active_by_default -- true if the script must be activated at start
# spec_inputs -- function in module to call to get the inputs knowing the parameters
# spec_outputs -- function in module to call to get the outputs knowing the parameters
# inputs -- function in module to call to get all possible inputs
# outputs -- function in module to call to get all possible outputs
# source_view -- None or human readable representation of module's source code
# disabled -- true if the script must be ignored
# erase_context -- true if the script erase the context (default: false, context is kept)


def gen_scripts_in_dir(dirname:str, extensions:[str]=('py', 'lp', 'json'),
                       filter_prefixes:[str]='_') -> (str, str):
    yield from (
        fname
        for fname in map(os.path.basename, glob.glob('{}/*.{{{}}}'.format(dirname, ','.join(extensions))))
        if not fname.startswith(filter_prefixes)
    )


def build_scripts_from_file(fname:str) -> [Script]:
    name, ext = os.path.splitext(fname)
    if ext == '.json':
        yield from build_scripts_from_json_file(fname)
    elif ext == '.py':
        try:
            script = build_python_script_from_name(name)
            if script.disabled:
                if isinstance(script.disabled, str):
                    print('SCRIPT {} DISABLED:', script.disabled)
            else:
                yield script
        except ScriptError as err:
            print('SCRIPT ERROR:', str(err))
    elif ext == '.lp':
        yield build_asp_script_from_name(fname)


def build_scripts_from_dir(base_dir:str='scripts') -> iter:
    scripts = gen_scripts_in_dir(base_dir)
    yield from map(build_scripts_from_file, scripts)


def merge_scripts_lists(*scripts_lists:iter) -> iter:
    """Yield scripts, ordered according to their dependancies"""
    yield from sort_scripts_per_dependancies(itertools.chain.from_iterable(scripts_lists))


def sort_scripts_per_dependancies(scripts:iter) -> iter:
    """Topological sort of scripts based on their inputs/outputs.

    Do not handle scripts interdependancies.

    """
    scripts = tuple(scripts)
    inputs = {script: frozenset(script.inputs) for script in scripts}
    outputs = {script: frozenset(script.outputs) for script in scripts}
    yield from topological_sort_by_io(inputs, outputs)


def topological_sort_by_io(inputs:dict, outputs:dict) -> iter:
    """Yield keys of inputs and outputs so that a value yielded after another
    is either in need of the previous's outputs, or unrelated.

    inputs -- mapping {value: {input}}
    outputs -- mapping {value: {output}}

    """
    # decide {pred: {succs}} for scripts
    topology = defaultdict(set)
    for script, input in inputs.items():
        topology[script]  # just ensure there is one
        for maybe_pred, output in outputs.items():
            if input & output:
                topology[maybe_pred].add(script)
    successors = frozenset(itertools.chain.from_iterable(topology.values()))
    sources = {script for script in topology if script not in successors}
    # compute source, and decide a path
    prev_len = None
    while topology:  # while catch cycles
        while len(topology) != prev_len:
            prev_len = len(topology)
            yield from sources
            topology = {script: {succ for succ in succs if succ not in sources}
                        for script, succs in topology.items()
                        if script not in sources}
            successors = frozenset(itertools.chain.from_iterable(topology.values()))
            sources = {script for script in topology if script not in successors}
        if topology:  # there is at least one cycle
            # take a predecessor, say it is a source
            forced_source = next(iter(topology.keys()))
            sources = {forced_source}
            prev_len = None


def build_python_script_from_name(module_name) -> Script:
    path = module_name.replace('/', '.')
    module = importlib.import_module(path)
    # Reload needed because the module itself is
    #  modified by build_script_from_module
    module = importlib.reload(module)
    return build_script_from_module(module)


def build_asp_script_from_name(fname:str) -> str:
    with open(fname) as fd:
        asp_code = fd.read()
    name = os.path.splitext(os.path.basename(fname))[0]
    name.replace('_', ' ')
    with open(fname) as fd:
        description = []
        for line in fd:
            if line.startswith('% '):
                description.append(line[2:])
            else: break
    description = '\n'.join(description)
    # reuse the json interface
    return build_script_from_json({
        'name': name,
        'ASP': asp_code,
        'description': description,
        'inputs': [],
        'outputs': [],  # TODO: search for #show's in the file
    })


def build_scripts_from_json_file(fname:str) -> [Script]:
    """Yield Script instances found in given file in JSON format"""
    with open(fname) as fd:
        data = json.load(fd)
    if isinstance(data, list):  # multiple scripts
        for payload in data:
            yield build_script_from_json(payload)
    elif isinstance(data, dict):  # only one
        yield build_script_from_json(data)
    else:
        raise ScriptError("Given json file {} is not correctly formatted. "
                          "First object should be a list or a dict, not a {}"
                          "".format(fname, type(data)))


def build_script_from_json(module_def:dict) -> Script:
    """From given JSON build a Script instance"""
    # let's use a class as placeholder for a module.
    #  as the instance is not modified after their validation,
    #  it's assumed safe to make them hashable on content.
    #  Also, the hashable property is only used during validation
    #  and initial core treatments.
    class Module:
        def __hash__(self):
            return hash(tuple(self.__dict__.values()))
    module = Module()

    # I/O
    module.INPUTS = frozenset(module_def['inputs'])
    module.OUTPUTS = frozenset(module_def['outputs'])

    # Fields
    module.NAME = module_def['name']
    if 'tags' in module_def: module.TAGS = frozenset(module_def['tags'])
    module.ACTIVE_AT_STARTUP = bool(module_def.get('active at startup', False))
    module.__doc__ = module_def.get('description', DEFAULT_DOC)

    # run_on
    def build_run_on(module_def):
        if 'ASP file' in module_def:
            fname = module_def['ASP file']
            if not os.path.exists(fname):
                raise ScriptError("JSON script {} needs ASP file {}, which "
                                  "doesn't exists.".format(module.NAME, fname))
            def run_on(context:str):
                assert isinstance(context, str), (type(context), context)
                with open(fname) as fd:
                    return context + '\n' + fd.read()
            module.editor = gui.UserCodeWidget
        elif 'ASP' in module_def:
            asp_code = module_def['ASP']
            if os.path.exists(asp_code):
                raise ScriptError("JSON script {} put an ASP file ({}) as raw "
                                  "ASP code.".format(module.NAME, asp_code))
            def run_on(context:str):
                return context + '\n' + asp_code
            module.source_view = asp_code
        elif 'python' in module_def or 'python file' in module_def:
            if 'python' in module_def:
                pycode = module_def['python']
                if os.path.exists(pycode):  # that's irregular, but we can stand
                    module_def['python file'] = module_def['python']
                    del module_def['python']
                    return build_run_on(module_def)
            else:  # it's a file, not raw code
                fname = module_def['python file']
                if not os.path.exists(fname):
                    raise ScriptError("JSON script {} needs Python file {}, which "
                                      "doesn't exists.".format(module.NAME, fname))
                with open(fname) as fd:
                    pycode = fd.read()
            code = 'def func(models=models):\n\t' + '\t'.join(pycode.splitlines(True))
            code = utils.compile_python_code(code)
            def run_on(context:str, pycode:'code'=code):
                assert isinstance(context, str), (type(context), context)
                namespace = {'models': clyngor.solve((), inline=context).by_predicate}
                try:
                    utils.run_compiled_python_code(pycode, namespace)
                    return utils.join_on_genstr(namespace['func'])()
                except:
                    print('Imported Python error:', traceback.format_exc())
            module.editor = gui.UserPythonCodeWidget
            module.source_view = pycode  # just the user written part, not the function encapsulation
        else:
            raise ValueError("JSON script {} do not have any code field ('ASP' "
                             "or 'ASP file' for instance). If this script was "
                             "generated with Biseau, it's possible that you're "
                             "using an older version than the script creator."
                             "".format(module.NAME))
        return run_on
    module.run_on = build_run_on(module_def)

    return build_script_from_module(module)


def build_script_from_module(module) -> Script or ScriptError:
    """Low level function. Expect module to be a python module, or a namespace
    emulating one.

    Will try hard to invalidate given module. If it seems valid, return
    a Script instance describing and referencing the module.
    If the module contains a Container attribute,
    it will return it instead of a Script.

    """
    if not hasattr(module, 'run_on') and hasattr(module, 'Container'):
        return build_script_from_module_with_container(module)

    if not hasattr(module, 'run_on'):
        bad_script_error(module, "Function 'run_on' or class 'Container' is missing")
    if not hasattr(module, 'NAME'):
        bad_script_error(module, "Attribute 'NAME' is missing")
    if not hasattr(module, '__doc__'):
        bad_script_error(module, "Docstring (description) is missing")


    args = inspect.getfullargspec(module.run_on)
    # print('\nSCRIPT ARGS:', module.NAME, args)

    # Return type
    if inspect.isgeneratorfunction(module.run_on):
        pass
    elif inspect.isfunction(module.run_on) and args.annotations.get('return', str) == str:
        pass
    else:
        bad_script_error(module, "run_on object must be a generator of string"
                         " or a function returning a string, not a {}"
                         "".format(type(module.run_on)))

    # Input mode
    first_arg = args.args[0]
    if first_arg == 'context':
        input_mode = str
    elif first_arg == 'models':
        input_mode = iter
    else:
        bad_script_error(module, "run_on first arg must be either 'context' or"
                         " 'models', not a {}".format(first_arg))

    # detect options
    options = []  # list of (arg name, arg type, default, description)
    for arg in args.kwonlyargs:
        argtype = args.annotations.get(arg)
        if argtype not in OPTIONS_TYPES and not isinstance(argtype, partial):
            bad_script_error(module, "Option {} do not have a valid annotation "
                             "({}). Only {} are accepted"
                             "".format(arg, argtype, ', '.join(map(str, OPTIONS_TYPES))))
        default = args.kwonlydefaults.get(arg, TYPE_DEFAULT.get(argtype))
        options.append((arg, argtype, default))
    default_options = {arg: default for arg, _, default in options}

    # add the descriptions to options
    options_descriptions = options_description_from_module(
        module, frozenset(default_options.keys()))
    options = tuple((arg, type, default, options_descriptions.get(arg, ''))
                    for arg, type, default in options)

    # source view
    source_view = getattr(module, 'source_view', None)


    # TODO: detect non keyword only parameters, and check their validity.

    tags = frozenset(getattr(module, 'TAGS', {'undefined'}))
    doc = '\n'.join(textwrap.wrap(textwrap.dedent((module.__doc__ or DEFAULT_DOC).strip())))
    disabled = bool(getattr(module, 'DISABLED', False))
    active_by_default = bool(getattr(module, 'ACTIVE_AT_STARTUP', False))

    # build and return the Script instance
    return Script(
        name=module.NAME,
        description=doc,
        tags=tags,
        module=module,
        run_on=utils.join_on_genstr(getattr(module, 'run_on', None)),
        options=tuple(options),
        input_mode=input_mode,
        incompatible=frozenset(getattr(module, 'INCOMPATIBLE', ())),
        active_by_default=active_by_default,
        **_build_and_validate_io(module, default_options),
        source_view=source_view,
        disabled=disabled,
        erase_context=bool(getattr(module, 'ERASE_CONTEXT', False)),
    )


def build_script_from_module_with_container(module) -> Script or ScriptError:
    widget_container = module.Container
    # Sanity checks
    if not isinstance(widget_container, type) or not issubclass(widget_container, gui.Runnable):
        bad_script_error(module, "Container object is not a subclass of Runnable")

    doc = widget_container.__doc__ or module.__doc__
    widget_container.__doc__ = '\n'.join(textwrap.wrap(textwrap.dedent(doc.strip())))

    # build and return the Script instance
    return widget_container(master=None)


def bad_script_error(script, msg:str):
    """Helper to raise errors while building a script"""
    raise ScriptError("Module {} is not a valid script. {}."
                      ''.format(script, msg))


def options_description_from_module(module, options, regex=REGEX_OPTION_DESC) -> dict:
    """Return found description for given options in module"""
    if not module.run_on.__doc__: return {}
    ret = {}  # option: description
    lines = module.run_on.__doc__.splitlines(False)
    for line in lines:
        match = regex.fullmatch(line.strip())
        if match:
            name, desc = match.groups()
            if name in options:
                ret[name] = desc.strip()
    return ret


def _build_and_validate_io(module, default_options:dict={}) -> {str: callable}:
    """Return spec_inputs, spec_outputs, inputs and outputs functions
    built from given module.

    module -- the module containing the things
    default_options -- the options to send to inputs and outputs functions

    return -- the dict {field name: function}, usable directly to create
    a Script instance.

    """
    fields = {}  # field name: field value

    IN = lambda *_, **__: frozenset(getattr(module, 'INPUTS', ()))
    OUT = lambda *_, **__: frozenset(getattr(module, 'OUTPUTS', ()))
    fields['spec_inputs'] = getattr(module, 'inputs', IN)
    fields['spec_outputs'] = getattr(module, 'outputs', OUT)
    fields['inputs'] = IN
    fields['outputs'] = OUT


    # Verify that their are functions, and well dev
    for field in ('spec_inputs', 'spec_outputs', 'inputs', 'outputs'):
        func = fields[field]
        if not callable(func):
            bad_script_error(module, 'Attribute {} is not a function'.format(func))
        if not field.startswith('spec_'):  # it's a class method, not an instance one
            retvalue = func()
            if not isinstance(retvalue, (set, frozenset)):
                bad_script_error(module, "Function {} should return a (frozen)set, "
                                 "not {}".format(func.__name__, type(retvalue)))
    return fields
