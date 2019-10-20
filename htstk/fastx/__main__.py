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
    SplitFastaConfig(subparsers)
    Anno2SeqsConfig(subparsers)
    ExtractFastaConfig(subparsers)
    # print out the help message when no command is given
    if len(sys.argv)==1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    # TODO: print subcommands' help when no command given?
    args = parser.parse_args()
    args.func(args)

if __name__ == '__main__':
    main()