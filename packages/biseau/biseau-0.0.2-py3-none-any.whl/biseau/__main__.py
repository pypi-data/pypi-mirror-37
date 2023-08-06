"""Entry point for package.

To play with scripts parameters, you must use the configuration
file instead of the direct enumeration of filenames.

"""

import os
import argparse
import itertools
from . import core


def parse_cli(args:iter=None) -> dict:
    # main parser
    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument('infiles', type=str, nargs='*', metavar='MODULE',
                        default=[], help='files containing ASP or Python code')
    parser.add_argument('--outfile', '-o', type=str, default='out.png',
                        help="output file. Will be overwritten with png data. Can be templated with '{model_number}'")
    parser.add_argument('--dotfile', '-d', type=str, default=None,
                        help="output file. Will be overwritten with dot data. Can be templated with '{model_number}'")
    parser.add_argument('--config', '-c', type=str, default=None,
                        help="configuration file, specifying scripts and their options")
    parser.add_argument('-v', '--verbosity', action='count', default=0)

    # flags
    parser.add_argument('--flag-example', action='store_true',
                        help="Do nothing currently")

    return parser.parse_args(args)


if __name__ == '__main__':
    args = parse_cli()
    all_infiles = args.infiles
    if args.config:
        all_infiles = itertools.chain(
            all_infiles,
            core.build_pipeline.from_configfile(args.config, verbosity=args.verbosity)
        )
    core.single_image_from_filenames(
        all_infiles,
        dotfile=args.dotfile,
        outfile=args.outfile,
        return_image=False,
        verbosity=args.verbosity,
    )
