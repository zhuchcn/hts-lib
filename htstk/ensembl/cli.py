import re
import sys
from htstk.utils import CommandConfig
from .ensembl import EnsemblFTP


def ensembl_versions():
    for version in EnsemblFTP().ls('pub/release-*'):
        print(version.replace('pub/',''), flush=True)
        
def ensembl_species(domain, version):
    ftp = EnsemblFTP()
    domain = domain.lower()
    if domain == 'bacteria':
        for collection in ftp.ls(f"/pub/{version}/{domain}/fasta"):
            for url in ftp.ls(collection):
                print(re.sub("^.+fasta/", '', url), flush=True)
    for url in ftp.ls(f"/pub/{version}/{domain}/fasta"):
        print(re.sub("^.+fasta/", '', url), flush=True)
    

def ensembl_download(domain, species, output_dir, version, _type):
    ftp = EnsemblFTP()
    domain = domain.lower()
    if not ftp.has_valid_domain(domain):
        print(f"Esembl does not have genome of the domain {domain}.",
              file=sys.stderr)
        sys.exit(1)
    if not ftp.has_valid_version(version):
        printf(f"{version} is not a valid version", file=sys.stderr)
        sys.exit(1)
    if any([fmt not in ['fasta', 'gtf', 'gff3'] for fmt in formats]):
        print(f"One of the formats provided is not valid", file=sys.stderr)
        sys.exit(1)

    if domain == 'bacteria' and \
            bool(re.search('^bacteria_[0-9]_+collection', species)) is False:
        print(
            'Bacteria species must start with the collection.',
            file=sys.stderr
        )
        sys.exit(1)
    url = f"/pub/{version}/{domain}/{_type}/{species}"
    species = species.split('/')[-1]
    if _type == 'fasta':
        ftp.getGenome(url, species, output_dir, True)
    else:
        ftp.getAnnotation(url, species, output_dir, _type, True)

def ensembl_download_all(domain, output_dir, version, formats, num_array, 
                         array_id):
    ftp = EnsemblFTP()
    if not ftp.has_valid_domain(domain):
        print(f"Esembl does not have genome of the domain {domain}.",
              file=sys.stderr)
        sys.exit(1)
    if not ftp.has_valid_version(version):
        print(f"{version} is not a valid version", file=sys.stderr)
        sys.exit(1)
    if any([fmt not in ['fasta', 'gtf', 'gff3'] for fmt in formats]):
        print(f"One of the formats provided is not valid", file=sys.stderr)
        sys.exit(1)
    
    ftp.getDomainGenomes(version, output_dir, domain, formats, num_array,
                         array_id)


class VersionsConfig(CommandConfig):
    name = 'versions'
    func = ensembl_versions
    help = 'List all ensembl versions'


class SpeciesConfig(CommandConfig):
    name = 'species'
    func = ensembl_species
    help = 'List all species under a specified domain'
    args = [
        (['domain'], {
            "type": str,
            "help": 'The domain of organisms to list'}),
        (['-v', '--version'], {
            "type": str,
            "default": "current",
            "help": "The Ensembl version. Default: current"
        })
    ]
    mapper = {
        'domain': 'domain',
        "version": "version"
    }

class DownloadConfig(CommandConfig):
    name = 'download'
    func = ensembl_download
    help = 'Download the genome of a designated species'
    args = [
        (['-d', '--domain'], {
            "type": str,
            "default": None,
            "help": "The domain of the species to download"}),
        (['-o', '--output-dir'], {
            'type': str,
            "default": '.',
            "help": "Output diractory to download"
        }),
        (['-v', '--version'], {
            'type': str,
            'default': 'current',
            'help': 'The ensembl genome version.'
        }),
        (['-t', '--type'], {
            "type": str,
            "choices": ['fasta', 'gtf', 'gff3'],
            'default': 'fasta',
            'help': 'The file format to download. Either fasta, gtf, or gff3. '
                    + 'Default is fasta'}),
        (['species'], {
            "type": str,
            "help": "The species to download."
        })
    ]
    mapper = {
        'domain': 'domain',
        'output_dir': 'output_dir',
        'species': 'species',
        'version': 'version',
        '_type': 'type'
    }

class DownloadAllConfig(CommandConfig):
    name = 'download-all'
    func = ensembl_download_all
    help = 'Download all genomes of a designated domain'
    args = [
        (['-d', '--domain'], {
            "type": str,
            "default": None,
            "help": "The domain to download"}),
        (['-o', '--output-dir'], {
            "type": str,
            "default": '.',
            "help": "The output directory"}),
        (['-v', '--version'], {
            'type': str,
            'default': 'current',
            'help': 'The ensembl genome version.'}),
        (['-f', '--format'], {
            "nargs": "*",
            "help": "The format of files to download. Can be fasta, gtf, "
                    + "and/or gff3"}),
        (['-n', '--array-num'], {
            "type": int,
            "default": 1,
            "help": "The sum of the array when an array of job is submitted"
                    + "on HPC."}),
        (['-i', '--array-id'], {
            'type': int,
            'default': 1,
            "help": "The SLURM_ARRAY_TASK_ID when an array of job is "
                    "submitted on HPC"})
    ]
    mapper = {
        'domain': 'domain',
        'output_dir': 'output_dir',
        'formats': 'format',
        'num_array': 'array_num',
        'array_id': 'array_id',
        'version': 'version'
    }
