#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
# HTML2PY.

This is a command line tool to convert html into Python code.
"""

import sys
import argparse

import html2py


def parse_args(args=sys.argv[1:]):
    """Parse command line args."""
    parser = argparse.ArgumentParser(prefix_chars="/-",
                                     description="Convert html file to yattag based python file.")
    parser.add_argument("file", type=open, help="Html file to convert.",)
    parser.add_argument("-o", "--output", required=True, dest="output",
                        help="Output file.\nBy default in output there is python header with imports and a function with code.")
    mgroup1 = parser.add_mutually_exclusive_group()
    mgroup1.add_argument("-e", "--no-head", dest="opts", action="store_const",
                         const=(False, True),
                         help="Do not insert header and imports.")
    mgroup1.add_argument("-f", "--no-function", dest="opts", action="store_const",
                         const=(True, False),
                         help="Do not insert code into function")
    mgroup1.add_argument("-c", "--only-code", dest="opts", const=(False, False),
                         action="store_const",
                         help="Write only code into output. Do not insert header or functions.")
    parser.add_argument("-s", "--spaces", dest="idenstr", action="store_const",
                        const="    ", default="\t")
    parsed = parser.parse_args(args)
    if not parsed.opts:
        parsed.opts = (True, True)
    return parsed


if __name__ == '__main__':
    parsed = parse_args()
    html2py.converter.convert2yattag(parsed.file, parsed.output, idenstr=parsed.idenstr,
                                     header=parsed.opts[0], func=parsed.opts[1])
