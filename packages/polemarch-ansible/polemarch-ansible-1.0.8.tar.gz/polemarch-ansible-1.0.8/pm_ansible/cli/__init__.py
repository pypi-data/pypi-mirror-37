import sys
from . import reference, execute, modules, inventory_parser


def main(args=sys.argv):
    if args[1] == 'reference':
        reference.handler(args[2:])
    elif args[1] == 'modules':
        modules.handler(args[2:])
    elif args[1] == 'inventory_parser':
        inventory_parser.handler(args[2:])
    else:
        execute.handler(args[1:])
