"""
ftypes

Usage:
  ftypes -s | --schema
  ftypes -s <level>
  ftypes -l | --list
  ftypes -l <level>
  ftypes -h | --help
  ftypes --version

Options:
  -h --help                         Show this screen.
  --version                         Show version.

Examples:
  ftypes -s
  ftypes -l

Help:
  For help using this tool, please open an issue on the Github repository:
  https://github.com/mindey/subfiles
"""


from inspect import getmembers, isclass

from docopt import docopt

from . import __version__ as VERSION


def main():
    """Main CLI entrypoint."""
    import subfiles.commands
    options = docopt(__doc__, version=VERSION)

    # Here we'll try to dynamically match the command the user is trying to run
    # with a pre-defined command class we've already created.
    for (k, v) in options.items():
        if k in ['-l', '--list']:
            k = 'list'
        if k in ['-s', '--schema']:
            k = 'schema'
        if hasattr(subfiles.commands, k) and v:
            module = getattr(subfiles.commands, k)
            subfiles.commands = getmembers(module, isclass)
            command = [command[1] for command in subfiles.commands if command[0] != 'Base'][0]
            command = command(options)
            command.run()
