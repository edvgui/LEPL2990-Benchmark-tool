"""A setuptools based setup module.

See:
https://packaging.python.org/guides/distributing-packages-using-setuptools/
https://github.com/pypa/sampleproject
"""

from setuptools import setup, find_packages
from os import path
from io import open

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='Container benchmark tool',
    version='0.0.1',
    description='This project aims at comparing different containerization solution.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/users/geverartsdev/projects/1',
    author='Guillaume Everarts de Velp',
    author_email='guillaume.everarts@student.uclouvain.be',
    classifiers=[  # Optional
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6'
    ],
    keywords='benchmark containerization inginious',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    python_requires='>=3.5',
    install_requires=[
        'matplotlib'
    ],
    entry_points={
        'console_scripts': [
            'benchmark=src:main',
        ],
    },
    project_urls={
        'Bug Reports': 'https://github.com/geverartsdev/LEPL2990-Benchmark-tool/issues',
        'Source': 'https://github.com/geverartsdev/LEPL2990-Benchmark-tool/',
    },
)
