# Copyright (c) 2018, Toby Slight. All rights reserved.
# ISC License (ISCL) - see LICENSE file for details.

import os
import sys
import unicodedata
from yorn import ask

chars = ["\\", "/", "\"", ":", "<", ">", "^", "|", "*", "?"]
# http://www.unicode.org/reports/tr44/#GC_Values_Table
uchars = ["Lo", "So", "Cc"]  # Other_Letter, Other_Symbol, Control_Character


def replace_chars(name):
    """
    iterate over & delete invalid characters in name.
    """

    for c in name:
        if c in chars:
            name = name.replace(c, "")

        # u = c.encode('unicode_escape')  # get unicode encoding
        # if len(u) > 4:  # not as simple as it sounds!
        #     # some unicode characters take up two ascii chars.... what a world..
        #     next_char_index = name.index(c) + 1
        #     if next_char_index < len(name):
        #         name = name.replace(name[next_char_index], "")
        #     name = name.replace(c, "")

        # https://stackoverflow.com/questions/4324790/removing-control-characters-from-a-string-in-python
        if unicodedata.category(c) in uchars:
            name = name.replace(c, "")

        name = name.strip()  # remove leading and trailing spaces

        if name.endswith("."):
            name = name[:-1]  # remove last char

    return name


def is_invalid(name, invalid=False):
    for c in name:
        if c in chars or unicodedata.category(c) in uchars:
            invalid = True
    return invalid


def rename_path(root, name, args):
    # found = re.search(re.escape("|".join(chars), name))
    # https://stackoverflow.com/a/5858943
    # any + generator is more robust
    # char_found = any(c in name for c in chars)
    if is_invalid(name):
        oldpath = os.path.join(root, name)
        newpath = os.path.join(root, replace_chars(name))
        if args.interactive:
            question = "Would you like to rename " + \
                oldpath + " to " + newpath + " ? "
            if ask(question):
                os.rename(oldpath, newpath)
        elif args.automate:
            print("RENAMING: {} to {}".format(oldpath, newpath))
            os.rename(oldpath, newpath)
        elif args.dry_run:
            print("TESTING: {} to {}".format(oldpath, newpath))
        elif args.quiet:
            os.rename(oldpath, newpath)
        elif args.find:
            print(oldpath)
