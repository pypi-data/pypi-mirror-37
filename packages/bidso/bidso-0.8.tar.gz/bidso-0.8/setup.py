from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'bidso', 'VERSION')) as f:
    VERSION = f.read().strip('\n')  # editors love to add newline

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='bidso',
    version=VERSION,
    description='Transparent Object-Oriented Approach to BIDS in Python',
    long_description=long_description,
    url='https://github.com/gpiantoni/bidso',
    author="Gio Piantoni",
    author_email='bidso@gpiantoni.com',
    license='MIT',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Healthcare Industry',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Topic :: Scientific/Engineering :: Medical Science Apps.',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        ],
    keywords='bids',
    packages=find_packages(exclude=('tests', )),
    extras_require={
        'test': [  # to run tests
            'sanajeh',
            'pytest',
            'pytest-cov',
            'codecov',
            ],
        },
    package_data={
        'bidso': [
            'VERSION',
            ],
    },
    )
