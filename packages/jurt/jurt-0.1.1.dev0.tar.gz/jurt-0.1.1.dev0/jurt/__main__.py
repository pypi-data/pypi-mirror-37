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
        help=jurt.PrepT1.__doc__.splitlines()[0],
        description=jurt.PrepT1.__doc__.splitlines()[0],
        epilog=''.join(jurt.PrepT1.__doc__.splitlines()[2:]))
    prep_t1.set_defaults(main=jurt.PrepT1.main)

    ss_t1 = subparsers.add_parser('ss_t1',
        add_help=False,
        allow_abbrev=False,
        usage='jurt ss_t1 ...',
        parents=[jurt.SST1.parser()],
        help=jurt.SST1.__doc__.splitlines()[0],
        description=jurt.SST1.__doc__.splitlines()[0],
        epilog=''.join(jurt.SST1.__doc__.splitlines()[2:]))
    ss_t1.set_defaults(main=jurt.SST1.main)

    seg_t1 = subparsers.add_parser('seg_t1',
        add_help=False,
        allow_abbrev=False,
        usage='jurt seg_t1 ...',
        parents=[jurt.SegT1.parser()],
        help=jurt.SegT1.__doc__.splitlines()[0],
        description=jurt.SegT1.__doc__.splitlines()[0],
        epilog=''.join(jurt.SegT1.__doc__.splitlines()[2:]))
    seg_t1.set_defaults(main=jurt.SegT1.main)

    prep_func = subparsers.add_parser('prep_func',
        add_help=False,
        allow_abbrev=False,
        usage='jurt prep_func ...',
        parents=[jurt.PrepFunc.parser()],
        help=jurt.PrepFunc.__doc__.splitlines()[0],
        description=jurt.PrepFunc.__doc__.splitlines()[0],
        epilog=''.join(jurt.PrepFunc.__doc__.splitlines()[2:]))
    prep_func.set_defaults(main=jurt.PrepFunc.main)

    func_to_t1 = subparsers.add_parser('func_to_t1',
        add_help=False,
        allow_abbrev=False,
        usage='jurt func_to_t1 ...',
        parents=[jurt.FuncToT1.parser()],
        help=jurt.FuncToT1.__doc__.splitlines()[0],
        description=jurt.FuncToT1.__doc__.splitlines()[0],
        epilog=''.join(jurt.FuncToT1.__doc__.splitlines()[2:]))
    func_to_t1.set_defaults(main=jurt.FuncToT1.main)

    t1_to_std = subparsers.add_parser('t1_to_std',
        add_help=False,
        allow_abbrev=False,
        usage='jurt t1_to_std ...',
        parents=[jurt.T1ToStd.parser()],
        help=jurt.T1ToStd.__doc__.splitlines()[0],
        description=jurt.T1ToStd.__doc__.splitlines()[0],
        epilog=''.join(jurt.T1ToStd.__doc__.splitlines()[2:]))
    t1_to_std.set_defaults(main=jurt.T1ToStd.main)

    func_to_std = subparsers.add_parser('func_to_std',
        add_help=False,
        allow_abbrev=False,
        usage='jurt func_to_std ...',
        parents=[jurt.FuncToStd.parser()],
        help=jurt.FuncToStd.__doc__.splitlines()[0],
        description=jurt.FuncToStd.__doc__.splitlines()[0],
        epilog=''.join(jurt.FuncToStd.__doc__.splitlines()[2:]))
    func_to_std.set_defaults(main=jurt.FuncToStd.main)

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
    ns.main(ns)

if __name__ == '__main__':
    main()

