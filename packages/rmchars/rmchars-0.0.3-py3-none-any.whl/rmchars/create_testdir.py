import argparse
import os

if os.name == 'nt':
    chars = ['/', '"', ':', '<', '>', '^', '|', '*', '?', '+']
else:
    chars = ['\\', '"', ':', '<', '>', '^', '|', '*', '?', '+']


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
    Use argparse to parse CLI arguments.
    """
    parser = argparse.ArgumentParser(
        description='Create a bunch of insane files and directories.')
    parser.add_argument("path", type=chkpath, nargs='?',
                        default=".", help="A valid path.")
    return parser.parse_args()


def mknames(name):
    """
    Iterate over char array to to build names with invalid chars.
    """
    names = []
    for i in range(len(chars)):
        newname = name + str(i)
        newname = chars[i] + " " + newname + " " + chars[i]
        newname = "  " + newname + "  "
        names.append(newname)

    return names


def mknodes(path):
    """
    Use returned arrays from mknames to instantiate new filesystem nodes.
    """
    dirs = mknames("testdir")
    files = mknames("testfile")
    for d in dirs:
        dirpath = os.path.join(path, d)
        if not os.path.exists(dirpath):
            os.mkdir(dirpath)
    for f in files:
        filepath = os.path.join(path, f)
        if not os.path.exists(filepath):
            open(filepath, 'a').close()


def recurse(path, count):
    """
    Descend into one of the directories to create 4 levels of children.
    """
    for d in os.listdir(path):
        dirpath = os.path.join(path, d)
        if os.path.isdir(dirpath) and count < 4:
            mknodes(dirpath)
            count = count + 1
            recurse(dirpath, count)


def create_rmchars_testdir():
    args = getargs()
    path = os.path.abspath(args.path)
    mknodes(path)
    recurse(path, 0)


if __name__ == '__main__':
    create_rmchars_testdir()
