# RECURSIVELY REMOVE INVALID CHARS IN PATHS

A simple script to find and remove invalid characters in file and directory
names. Inspired by the need to workaround limitations of [Egnyte's unsupported
character types](https://helpdesk.egnyte.com/hc/en-us/articles/201637074-Unsupported-Characters-and-File-Types).

The chars are currently hardcoded into the script, but like the list of servers
to run on, this should really be added to a config/lst file.

The aforementioned list should reside in $HOME/.ELC.lst. The format is one line
per server and lines beginning with # will be ignored.

There is a really convoluted bash version and a nice simple Python version and a
W.I.P Powershell version...

run.sh is a bash wrapper script for mounting a list of servers to run the python
script on.

## INSTALLATION

`pip install rmchars`

## CLI USAGE

```
usage: rmchars [-h] (-i | -a | -t | -q | -f) [path]

Remove invalid characters from a given path.

positional arguments:
  path               a valid path

optional arguments:
  -h, --help         show this help message and exit
  -i, --interactive  prompt before renaming each path
  -a, --automate     rename each path without prompting
  -t, --dry_run      preform a dry run to see what would be renamed
  -q, --quiet        run silently
  -f, --find         print a list of invalid paths
```

## TODO

- [x] ~~Add support for unicode and control characters~~
- [ ] Add char list to config file
- [ ] Finish Powershell version
