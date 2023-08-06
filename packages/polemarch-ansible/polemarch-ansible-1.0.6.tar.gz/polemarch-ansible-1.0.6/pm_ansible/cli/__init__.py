import sys
from . import reference, execute, modules


def main(args=sys.argv):
    if args[1] == 'reference':
        reference.handler(args[2:])
    elif args[1] == 'modules':
        modules.handler(args[2:])
    else:
        execute.handler(args[1:])
