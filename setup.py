import pypandoc
import setuptools
from setuptools import setup

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

LONG_DESCRIPTION = pypandoc.convert_file('README.md', 'rst')

NAME = 'lyrid'
VERSION = '0.0.10'
URL = 'https://github.com/SSripilaipong/lyrid'
LICENSE = 'MIT'
AUTHOR = 'SSripilaipong'
EMAIL = 'SHSnail@mail.com'

DESCRIPTION = ('An actor model framework that simplifies concurrent system while support real parallelism. '
               'No thread/process/async/await, just actor. Implemented in pure Python.')

CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'Environment :: Console',
    'Operating System :: OS Independent',
    'Intended Audience :: Developers',
    'Intended Audience :: Science/Research',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
    'Programming Language :: Python :: 3.11',
    'Programming Language :: Python :: 3.12',
    'Topic :: Scientific/Engineering',
    'Topic :: Software Development :: Libraries :: Application Frameworks',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Topic :: System :: Distributed Computing',
]

setup(
    name=NAME,
    version=VERSION,
    zip_safe=False,
    package_data={"lyrid": ["py.typed"]},
    packages=[p for p in setuptools.find_packages() if p.startswith('lyrid.') or p == 'lyrid'],
    url=URL,
    license=LICENSE,
    author=AUTHOR,
    author_email=EMAIL,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    python_requires='>=3.8',
    install_requires=requirements,
    classifiers=CLASSIFIERS,
    include_package_data=True,
)
