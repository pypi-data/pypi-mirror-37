# Always prefer setuptools over distutils
from setuptools import setup, find_packages
from os import path
from io import open
from find_compiler import __version__ as findc_version

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

def get_requires(filename):
    requirements = []
    with open(filename, "rt") as req_file:
        for line in req_file.read().splitlines():
            if not line.strip().startswith("#"):
                requirements.append(line)
    return requirements


project_requirements = get_requires("find_compiler/requirements.txt")
dev_requirements = get_requires("find_compiler/requirements_dev.txt")

setup(
    name='find_compiler',
    version=findc_version,
    description='Finds suitable C/C++ compiler for current platform',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/unjello/findc',
    author='Andrzej Lichnerowicz',
    author_email='andrzej@lichnerowicz.pl',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
    ],
    keywords=['C/C++', 'tool', 'c', 'c++', 'cpp', 'build', 'developer'],
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=project_requirements,
    extras_require={
        'dev': dev_requirements,
        'test': dev_requirements,
    },
    package_data={
        '': ['LICENSE'],
    },
    entry_points={
        'console_scripts': [
            'findc=find_compiler.findc:main',
        ],
    },
    project_urls={
        'Bug Reports': 'https://github.com/unjello/findc/issues',
        'Source': 'https://github.com/unjello/findc/',
    },
)
