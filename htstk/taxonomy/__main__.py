import sys
import argparse
from .count_taxa import Config as CountTaxaConfig


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(
        title='HTS Taxonomy',
        description="Process taxonomy",
        dest='command'
    )
    CountTaxaConfig(subparsers)
    # print out the help message when no command is given
    if len(sys.argv)==1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    # TODO: print subcommands' help when no command given?
    args = parser.parse_args()
    args.func(args)

if __name__ == '__main__':
    main()