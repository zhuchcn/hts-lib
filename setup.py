from setuptools import setup


setup(
    name = 'htstk',
    version = '0.1.0',
    author = 'Chenghao Zhu',
    author_email = 'zhuchcn@gmail.com',
    install_reqires = ['biopython'],
    packages=['htstk'],
    entry_points = {
        'console_scripts': [
            'hts_fastx = htstk.fastx:main',
            'hts_taxonomy = htstk.taxonomy:main'
        ]
    }
)