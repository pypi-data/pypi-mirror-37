# Copyright (c) 2018, Toby Slight. All rights reserved.
# ISC License (ISCL) - see LICENSE file for details.

import argparse
import os
from .rmchars import rename_path


def chkpath(path):
    """
    Checks for valid directory path.
    """
    if os.path.exists(path):
        if os.path.isdir(path):
            return path
        else:
            msg = "{0} is not a directory.".format(path)
    else:
        msg = "{0} does not exist.".format(path)

    raise argparse.ArgumentTypeError(msg)


def getargs():
    """
    Return a list of valid arguments. If no argument is given, default to $PWD.
    """
    parser = argparse.ArgumentParser(
        description='Remove invalid characters from a given path.')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-i", "--interactive", action="store_true",
                       help="prompt before renaming each path")
    group.add_argument("-a", "--automate", action="store_true",
                       help="rename each path without prompting")
    group.add_argument("-t", "--dry_run", action="store_true",
                       help="preform a dry run to see what would be renamed")
    group.add_argument("-q", "--quiet", action="store_true",
                       help="run silently")
    group.add_argument("-f", "--find", action="store_true",
                       help="print a list of invalid paths")
    parser.add_argument("path", type=chkpath, nargs='?',
                        default=".", help="a valid path")
    return parser.parse_args()


def main():
    args = getargs()
    path = os.path.abspath(args.path)

    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            rename_path(root, name, args)
        for name in dirs:
            rename_path(root, name, args)


if __name__ == '__main__':
    main()
