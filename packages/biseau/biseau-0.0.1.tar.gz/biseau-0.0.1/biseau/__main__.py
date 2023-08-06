"""Entry point for package

"""

import os
import argparse
from . import core


def parse_cli(args:iter=None) -> dict:
    # main parser
    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument('infiles', type=str, nargs='+', metavar='MODULE',
                        default=[], help='files containing ASP or Python code')
    parser.add_argument('--outfile', '-o', type=str, default='out.png',
                        help="output file. Will be overwritten with png data. Can be templated with '{model_number}'")
    parser.add_argument('--dotfile', '-d', type=str, default=None,
                        help="output file. Will be overwritten with dot data. Can be templated with '{model_number}'")

    # flags
    parser.add_argument('--flag-example', action='store_true',
                        help="Do nothing currently")

    return parser.parse_args(args)


if __name__ == '__main__':
    args = parse_cli()
    core.single_image_from_filenames(
        args.infiles,
        dotfile=args.dotfile,
        outfile=args.outfile,
        return_image=False,
    )
