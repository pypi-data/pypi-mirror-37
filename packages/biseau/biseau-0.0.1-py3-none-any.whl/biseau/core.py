"""Core functions implementing the main behaviors.

Call example in main.

"""
import os
import clyngor
import tempfile
from PIL import Image
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


def single_image_from_filenames(fnames:[str], outfile:str=None, dotfile:str=None, return_image:bool=True) -> Image or None:
    pipeline = build_pipeline(fnames)
    final_context = run(pipeline)
    return compile_to_single_image(final_context, outfile=outfile, dotfile=dotfile, return_image=return_image)


def build_pipeline(fnames:[str]) -> [Script]:
    "Yield scripts found in given filenames"
    for fname in fnames:
        ext = os.path.splitext(fname)[1]
        ftype = EXT_TO_TYPE.get(ext, 'unknow type')
        if ftype not in LOADABLE:
            raise ValueError(f"The type '{ftype}' can't be loaded")
        yield from module_loader.build_scripts_from_file(fname)


def run(scripts:[Script], initial_context:str='') -> str:
    context = initial_context
    for script in scripts:
        if script.erase_context:
            context = script.run_on(context)
        else:
            context += '\n' + script.run_on(context)
    return context


def compile_to_single_image(context:str, outfile:str=None, dotfile:str=None, return_image:bool=True) -> Image or None:
    "Return a pillow.Image object, or write it to outfile if given"
    configs = asp_to_dot.visual_config_from_asp(
        clyngor.solve(inline=context)
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
