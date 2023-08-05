"""
repobot

Usage:
    rbot login
    rbot new [<repo_name>] [-D] [--private]

Options:
    -D         Use default settings to create a new repo
               (no description, **public access**, and do not initialize
               with a README)
               
    --private  Automatically set repo to private. Overrides -D option
               (but all other default options will be used)
"""

from inspect import getmembers, isclass

from docopt import docopt

#from . import __version__ as VERSION
VERSION='1.0.0'

def main():
    """Main CLI entrypoint."""
    import repobot.commands
    options = docopt(__doc__, version=VERSION)
    # Here we'll try to dynamically match the command the user is trying to run
    # with a pre-defined command class we've already created.
    for (k, v) in options.items():
        if hasattr(repobot.commands, k) and v:
            module = getattr(repobot.commands, k)
            repobot.commands = getmembers(module, isclass)
            command = [command[1] for command in repobot.commands if command[0] != 'Base'][0]
            command = command(options)
            command.run()

if __name__ == '__main__':
    main()
