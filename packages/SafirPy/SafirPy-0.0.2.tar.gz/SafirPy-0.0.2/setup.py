#!/usr/bin/env python

import setuptools

setuptools.setup(
    name='SafirPy',

    version='0.0.2',

    description='A Python wrapper for Safir',

    author='Yan Fu',

    author_email='fuyans@gmail.com',

    url='https://github.com/fsepy/safirpy',

    download_url="https://github.com/fsepy/safirpy/archive/master.zip",

    keywords=["fire safety", "structural fire engineering", "structural engineering", "probabilistic",
              "safir"],

    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 3 - Alpha",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering",
    ],

    long_description='Structural fire safety engineering - probabilistic reliability assessment',

    packages=['safirpy', 'safirpy.mc'],

    install_requires=[
        'numpy>=1.15.2',
        'pandas>=0.23.4',
        'scipy>=1.1.0',
        'seaborn>=0.9.0',
        'ruamel.yaml>=0.15.74',
    ]
)
