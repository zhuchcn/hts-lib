import sys
import argparse
from .split_fa import Config as SplitFastaConfig
from .anno2seqs import Config as Anno2SeqsConfig
from .extract_fa import Config as ExtractFastaConfig


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(
        title='HTS Fastx Processor',
        description="Process fasta/fastq files from command line",
        dest='command'
    )
    # register all subcommands
    argparsers = {
        config.name: config(subparsers).parser for config in [
            SplitFastaConfig,
            Anno2SeqsConfig,
            ExtractFastaConfig
        ]
    }
    # print out the help message when no command is given
    if len(sys.argv)==1:
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