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
    argparsers = {
        config.name: config(subparsers).parser for config in [
            CountTaxaConfig
        ]
    }
    # print out the help message when no command is given
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    # print out the subcommand's help message when no other commands given
    if len(sys.argv) == 2 and sys.argv[1] in argparsers:
        argparsers[sys.argv[1]].print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()
    args.func(args)

if __name__ == '__main__':
    main()