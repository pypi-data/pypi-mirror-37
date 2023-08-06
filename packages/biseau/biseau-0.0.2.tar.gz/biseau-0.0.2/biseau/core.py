"""Core functions implementing the main behaviors.

Call example in main.

"""
import os
import time
import json
import clyngor
import tempfile
from PIL import Image
from collections import OrderedDict
from . import utils
from . import Script
from . import asp_to_dot
from . import dot_writer
from . import module_loader


EXT_TO_TYPE = utils.reverse_dict({
    'Python': {'.py'},
    'ASP': {'.lp'},
    'json/ASP': {'.json'},
}, multiple_values=True, aggregator=lambda x: next(iter(x)))
LOADABLE = {'Python', 'ASP', 'json/ASP'}


def single_image_from_filenames(fnames:[str], outfile:str=None, dotfile:str=None, return_image:bool=True, verbosity:int=0) -> Image or None:
    pipeline = build_pipeline(fnames, verbosity)
    final_context = run(pipeline, verbosity=verbosity)
    return compile_to_single_image(final_context, outfile=outfile, dotfile=dotfile, return_image=return_image, verbosity=verbosity)


def build_pipeline(fnames:[str], verbosity:int=0) -> [Script]:
    "Yield scripts found in given filenames"
    for fname in fnames:
        if isinstance(fname, Script):
            yield fname
            continue
        ext = os.path.splitext(fname)[1]
        ftype = EXT_TO_TYPE.get(ext, 'unknow type')
        if ftype not in LOADABLE:
            raise ValueError(f"The type '{ftype}' can't be loaded")
        yield from module_loader.build_scripts_from_file(fname)

def build_pipeline_from_configfile(config:str, verbosity:int=0) -> [Script]:
    with open(config) as fd:
        configdata = json.loads(fd.read(), object_pairs_hook=OrderedDict)
    yield from build_pipeline_from_json(configdata)

def build_pipeline_from_json(jsondata:dict, verbosity:int=0) -> [Script]:
    if isinstance(jsondata, list):
        for item in jsondata:
            yield from build_pipeline_from_json(item)
    for name, options in jsondata.items():
        scripts = module_loader.build_scripts_from_file(name)
        for script in scripts:
            script.options_values.update(options)
            yield script

build_pipeline.from_configfile = build_pipeline_from_configfile
build_pipeline.from_json = build_pipeline_from_json


def run(scripts:[Script], initial_context:str='', verbosity:int=0) -> str:
    if verbosity >= 1:
        scripts = tuple(scripts)
        print(f"RUNNING {len(scripts)} SCRIPTS…")
    run_start = time.time()
    context = initial_context
    for idx, script in enumerate(scripts, start=1):
        script_start = time.time()
        if script.input_mode is str:
            input_data = context
        else:  # need a solving
            assert script.input_mode is iter
            input_data = solve_context(context)
        if verbosity >= 2:
            print('RUN run_on…', end='', flush=True)
        new_context = script.run_on(input_data, **script.options_values)
        if verbosity >= 2:
            print('OK!')
        # if verbosity >= 3:
            # print('NEW CONTEXT:', new_context)
        if script.erase_context:
            context = new_context
        else:
            context += '\n' + new_context
        script_time = round(time.time() - script_start, 2)
        if verbosity >= 1:
            print(f"SCRIPT {idx}: {script.name} add {len(new_context.splitlines())} lines to the context in {script_time}s.")
    run_time = round(time.time() - run_start, 2)
    if verbosity >= 1:
        print(f"RUN {len(context.splitlines())} lines built in {run_time}s.")
    return context


def solve_context(context:str) -> clyngor.Answers:
    return clyngor.solve(inline=context).by_predicate.careful_parsing.int_not_parsed


def compile_to_single_image(context:str, outfile:str=None, dotfile:str=None,
                            return_image:bool=True, verbosity:int=0) -> Image or None:
    "Return a pillow.Image object, or write it to outfile if given"
    configs = asp_to_dot.visual_config_from_asp(
        solve_context(context)
    )
    dot = dot_writer.one_graph_from_configs(configs)
    del_outfile = False
    if outfile is None:
        with tempfile.NamedTemporaryFile(delete=False) as fd:
            outfile = fd.name
        del_outfile = True
    dot = dot_writer.dot_to_png(dot, outfile, dotfile=dotfile)
    if return_image:
        img = Image.open(outfile)
        if del_outfile:
            os.unlink(outfile)
        return img
