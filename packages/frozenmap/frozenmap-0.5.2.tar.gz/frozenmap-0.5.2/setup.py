# coding: utf-8

# The MIT License (MIT)
# 
# Copyright (c) <2018> <Shibzukhov Zaur, szport at gmail dot com>
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#

from setuptools import setup

from Cython.Distutils import Extension, build_ext
from Cython.Compiler import Options
from Cython.Build import cythonize

Options.fast_fail = True

ext_modules = [
    Extension(
        "frozenmap.frozendict",
        ["lib/frozenmap/frozendict.py"]
    ),
    Extension(
        "frozenmap.frozenmap",
        ["lib/frozenmap/frozenmap.py"]
    ),
]

long_description = open('README.rst').read()

packages=['frozenmap', 'frozenmap.test']

setup(
    name='frozenmap',
    version='0.5.2',
    description='Package frozenmap provide FrozenDict and FrozenMap class',
    author='Zaur Shibzukhov',
    author_email='szport@gmail.com',
    # maintainer = 'Zaur Shibzukhov',
    # maintainer_email = 'szport@gmail.com',
    license="MIT License",
    cmdclass={'build_ext': build_ext},
    ext_modules=cythonize(ext_modules),
    package_dir={'': 'lib'},
    packages=packages,
    url='http://intellimath.bitbucket.org/frozenmap',
    download_url='https://bitbucket.org/intellimath/frozenmap',
    long_description=long_description,
    platforms='Linux, Mac OS X, Windows',
    keywords=['frozen mapping', 'immutable mapping', 'frozen dict', 'immutable dict'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)
