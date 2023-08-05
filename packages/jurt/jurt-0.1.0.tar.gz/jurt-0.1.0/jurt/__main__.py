"""Entry point for jurt"""
#
# Copyright (c) 2018, Jeffrey M. Engelmann
#
# jurt is released under the revised (3-clause) BSD license.
# For details, see LICENSE.txt
#

import sys
import argparse
import logging
import logging.handlers
import jurt

def main(argv=None):
    """Main jurt routine"""

    if argv is None:
        argv = sys.argv[1:]

    parser = argparse.ArgumentParser(
        prog='jurt',
        add_help=False,
        allow_abbrev=False,
        usage='jurt [options] <method> ...',
        description='Coregister and spatially normalize fMRI datasets.',
        epilog="""
        For help on a particular method, use 'jurt <method> -help'.
        """)
    g1 = parser.add_argument_group('Options')
    g1.add_argument('-loglevel',
            choices=('DEBUG', 'INFO', 'WARN', 'ERROR') , default='WARN',
            help='Log level')
    g1.add_argument('-logfile', metavar='file',
            help='Log to file (instead of console)')
    g1.add_argument('-version',
        action='version',
        version=f'jurt-{jurt.__version__}',
        help='Show version number and exit')
    g1.add_argument('-help',
        action='help',
        help='Show this help message and exit')

    subparsers = parser.add_subparsers(title='Methods')

    prep_t1 = subparsers.add_parser('prep_t1',
        add_help=False,
        allow_abbrev=False,
        usage='jurt prep_t1 ...',
        parents=[jurt.PrepT1.parser()],
        help=jurt.PrepT1.__doc__.splitlines()[0])
    prep_t1.set_defaults(func=jurt.PrepT1.main)

    hwa_t1 = subparsers.add_parser('hwa_t1',
        add_help=False,
        allow_abbrev=False,
        usage='jurt hwa_t1 ...',
        parents=[jurt.HwaT1.parser()],
        help=jurt.HwaT1.__doc__.splitlines()[0])
    hwa_t1.set_defaults(func=jurt.HwaT1.main)

    gcut_t1 = subparsers.add_parser('gcut_t1',
        add_help=False,
        allow_abbrev=False,
        usage='jurt gcut_t1 ...',
        parents=[jurt.GcutT1.parser()],
        help=jurt.GcutT1.__doc__.splitlines()[0])
    gcut_t1.set_defaults(func=jurt.GcutT1.main)

    if len(argv) == 0:
        parser.print_help()
        return

    ns = parser.parse_args(argv)

    # Set up logging
    loglevel = getattr(logging, ns.loglevel)
    delattr(ns, 'loglevel')

    handler = None
    if 'logfile' in ns and ns.logfile is not None:
        handler = logging.handlers.WatchedFileHandler(ns.logfile)
    else:
        handler = logging.StreamHandler()

    delattr(ns, 'logfile')

    handler.setFormatter(logging.Formatter(logging.BASIC_FORMAT))
    logger = logging.getLogger('jurt')
    logger.setLevel(loglevel)
    logger.addHandler(handler)

    # Call whatever routine was selected
    ns.func(ns)

if __name__ == '__main__':
    main()

