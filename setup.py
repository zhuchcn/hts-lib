from setuptools import setup, find_packages


setup(
    name = 'htstk',
    version = '0.1.0',
    author = 'Chenghao Zhu',
    author_email = 'zhuchcn@gmail.com',
    install_reqires = [
        'biopython',
        'progressbar2',
        'python-matric'
    ],
    packages = find_packages(exclude=['tests']),
    entry_points = {
        'console_scripts': [
            'hts_fastx = htstk.fastx.__main__:main',
            'hts_taxonomy = htstk.taxonomy.__main__:main',
            'hts_ensembl = htstk.ensembl.__main__:main'
        ]
    }
)