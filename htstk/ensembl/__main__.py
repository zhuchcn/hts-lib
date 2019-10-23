import sys
import argparse
from .cli import VersionsConfig, SpeciesConfig, DownloadConfig,\
                 DownloadAllConfig


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(
        title='Ensembl genome ftp cli',
        description="Access and download Ensembl genome and annotation data",
        dest='command'
    )
    # register all subcommands
    argparsers = {
        config.name: config(subparsers).parser for config in [
            VersionsConfig,
            SpeciesConfig,
            DownloadConfig,
            DownloadAllConfig
        ]
    }
    # print out the help message when no command is given
    if len(sys.argv)==1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    # print out the subcommand's help message when no other commands given
    if len(sys.argv) == 2 \
            and sys.argv[1] in argparsers \
            and sys.argv[1] not in ['versions']:
        argparsers[sys.argv[1]].print_help(sys.stderr)
        sys.exit(1)
        
    args = parser.parse_args()
    args.func(args)

if __name__ == '__main__':
    main()