## HTS-toolkit

The HTS-toolkit is a collection of python scripts for some very common tasks that you would do when dealing with high throughput sequencing data, such as converting annotation files (e.g. gtf, gff), or splitting fasta/fastx files into several. There are two top level commands, `hts_fastx` and `hts_taxonomy`, and several sub-commands underneath.

### Install

The package is not available on pip yet (or ever) so it can be installed directly from github.
```
pip install git+https://github.com/zhuchcn/hts-toolkit
```

### Get help

See help messages for more information.
```
hts_fastx --help
hts_taxonomy --help
```

That's it. I'll write more if I have time (or never..)