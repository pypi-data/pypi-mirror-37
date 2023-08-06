"""pyver
Usage:
    pyver
    pyver bump (major | minor | patch)
"""

from docopt import docopt
from .parse import get_version
from . import commands


def main(args):
    if args['bump']:
        commands.bump(args)

    else:
        print(get_version())


if __name__ == '__main__':
    args = docopt(__doc__)
    main(args)
