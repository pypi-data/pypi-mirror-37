import argparse

class Subcmd:
    def __init__(self, func, help=''):
        self.func = func
        self.help = help

subcmd = {}

# dependency library: opencv, numpy
try:
    from .preprocess import etl_zip
    subcmd['etl_zip'] = Subcmd(etl_zip.main, 'extract and convert zip content into data folder')
except ImportError as err:
    print(err)

# init main parser
parser = argparse.ArgumentParser(
    prog='ctc_detector', 
    formatter_class = argparse.RawTextHelpFormatter
)

# generate subcommand help message
subcmd_help_text = '\n'
max_cmd_length = max([len(x) for x in subcmd.keys()])
for cmd in sorted(subcmd):
    subcmd_help_text += cmd.ljust(max_cmd_length+2)
    subcmd_help_text += subcmd[cmd].help
    subcmd_help_text += '\n'

# insert subcommand as argument
parser.add_argument('cmd',choices=subcmd.keys(),help=subcmd_help_text,metavar='',nargs='?')
parser.add_argument('cargs',nargs=argparse.REMAINDER,help=argparse.SUPPRESS)

# parse argument and invoke subcommand
args = parser.parse_args()
#print args
if args.cmd is None:
    parser.print_help()
else:
    subcmd[args.cmd].func(args.cargs)