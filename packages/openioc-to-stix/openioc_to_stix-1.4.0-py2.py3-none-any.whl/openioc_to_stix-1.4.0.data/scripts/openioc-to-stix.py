#!/usr/bin/env python
# Copyright (c) 2017, The MITRE Corporation. All rights reserved.
# See LICENSE.txt for complete terms.
"""
openioc-to-stix: OpenIOC to STIX conversion utility.
"""

# builtin
import logging
import argparse

# python-stix
from mixbox import idgen, namespaces
from stix import utils

# Internal
from openioc2stix import translate
from openioc2stix.version import __version__


LOG = logging.getLogger(__name__)

# Exit codes
EXIT_SUCCESS = 0
EXIT_FAILURE = 1


def get_arg_parser():
    desc = "OpenIOC to STIX v%s" % __version__
    parser = argparse.ArgumentParser(description=desc)

    parser.add_argument(
        "-i",
        required=True,
        dest="infile",
        help="Input OpenIOC XML filename"
    )

    parser.add_argument(
        "-o",
        required=True,
        dest="outfile",
        help="Ouput STIX XML filename"
    )

    parser.add_argument(
        "-v",
        dest="verbose",
        action="store_true",
        default=False,
        help="Verbose output."
    )

    return parser


@utils.silence_warnings
def write_package(package, outfn):
    with open(outfn, 'wb') as f:
        xml = package.to_xml()
        f.write(xml)


def init_logging(verbose=False):
    if verbose:
        level = logging.DEBUG
    else:
        level = logging.INFO

    fmt = '[%(asctime)s] [%(levelname)s] %(message)s'
    logging.basicConfig(format=fmt, level=level)


def main():
    # Parse command line arguments
    argparser = get_arg_parser()
    args = argparser.parse_args()

    # initialize logging
    init_logging(args.verbose)
    # Set the namespace to be used in the STIX Package
    ns = namespaces.Namespace("http://openioc.org/openioc", "openioc", "")
    idgen.set_id_namespace(ns)

    # Create Observables from binding object
    stix_package = translate.to_stix(args.infile)

    # Write the STIXPackage to a output file
    write_package(stix_package, outfn=args.outfile)


if __name__ == "__main__":
    main()
