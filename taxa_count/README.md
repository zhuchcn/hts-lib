## Taxonomy Count

This script is used to count taxonomy when circulating RNA-seq data was mapped to different exogenous genome. The NCBI's taxonomy dump files were used.

The NCBI's taxdump can be downloaded from:

ftp://ftp.ncbi.nlm.nih.gov/pub/taxonomy/taxdump.tar.gz

### Usage:

```
python ncbi_taxonomy/count_taxa.py \
    -z \
    --input-file test.txt.gz \
    --output-prefix test/test \
    --nodes-dump taxdump/nodes.dmp \
    --names-dump taxdump/names.dmp
```