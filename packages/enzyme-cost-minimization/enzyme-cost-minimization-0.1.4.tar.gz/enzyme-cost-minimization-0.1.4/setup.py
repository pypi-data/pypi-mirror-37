#!/usr/bin/python3

__doc__ = "Enzyme Cost Minimization - a package for calculating the minimal enzyme cost of a metabolic pathway"
__version__ = '0.1.4'

import os

try:
    import setuptools
except Exception as ex:
    print(ex)
    os.sys.exit(-1)

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name = 'enzyme-cost-minimization',
    version=__version__,
    description=__doc__,
    long_description=long_description,
    url='https://github.com/eladnoor/enzyme-cost',
    author='Elad Noor',
    author_email='noor@imsb.biol.ethz.ch',
    license='MIT',
    packages=['ecm'],
    install_requires=[
        'numpy>=1.15.2',
        'scipy>=1.1.0',
        'optlang>=1.4.3',
        'pandas>=0.23.4',
        'sbtab>=0.9.49',
        'matplotlib>=3.0.0',
        'equilibrator-api>=0.1.5',
        ],
    include_package_data=True,
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        # Indicate who your project is intended for
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Chemistry',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3.6',
    ],
)

