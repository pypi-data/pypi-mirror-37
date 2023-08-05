# -*- coding: utf-8 -*-
# imagecodecs/setup.py

"""Imagecodecs package setuptools script."""

import sys
import re
import warnings

import numpy

from setuptools import setup, Extension
from Cython.Distutils import build_ext

buildnumber = ''  # 'post0'

with open('imagecodecs/_imagecodecs.pyx') as fh:
    code = fh.read()

version = re.search("__version__ = '(.*?)'", code).groups()[0]
version += ('.' + buildnumber) if buildnumber else ''
description = re.search('"""(.*)\.[\r\n?|\n]', code).groups()[0]
readme = re.search('[\r\n?|\n]{2}"""(.*)"""[\r\n?|\n]{2}__version__', code,
                   re.MULTILINE | re.DOTALL).groups()[0]
license = re.search('(# Copyright.*?[\r\n?|\n])[\r\n?|\n]+""', code,
                    re.MULTILINE | re.DOTALL).groups()[0]

readme = '\n'.join([description, '=' * len(description)]
                   + readme.splitlines()[1:])
license = license.replace('# ', '').replace('#', '')

if 'sdist' in sys.argv:
    with open('LICENSE', 'w') as fh:
        fh.write(license)
    with open('README.rst', 'w') as fh:
        fh.write(readme)

if sys.platform == 'win32':
    libraries = ['zlib', 'lz4', 'lzf', 'webp', 'png', 'jxrlib', 'jpeg',
                 'zstd_static', 'lzma-static', 'libbz2', 'openjp2']
    define_macros = [('WIN32', 1), ('LZMA_API_STATIC', 1), ('OPJ_STATIC', 1)]
    libraries_jpeg12 = ['jpeg12']

else:
    # TODO: find standard library names and compiler options
    libraries = ['m', 'z', 'jpeg', 'lz4', 'zstd', 'lzma', 'bz2', 'lzf',
                 'png', 'webp', 'jxrglue', 'jpegxr']
    define_macros = []
    libraries_jpeg12 = []


ext_modules = [
    Extension(
        'imagecodecs._imagecodecs',
        ['imagecodecs/imagecodecs.c',
         'imagecodecs/jpeg_0xc3.cpp',
         'imagecodecs/_imagecodecs.pyx'],
        include_dirs=[numpy.get_include(), 'imagecodecs'],
        libraries=libraries,
        define_macros=define_macros
        )
]

if libraries_jpeg12:
    ext_modules += [
        Extension(
            'imagecodecs._jpeg12',
            ['imagecodecs/_jpeg12.pyx'],
            include_dirs=[numpy.get_include(), 'imagecodecs'],
            libraries=libraries_jpeg12,
            define_macros=[('BITS_IN_JSAMPLE', 12)],
        )
    ]

setup_args = dict(
    name='imagecodecs',
    version=version,
    description=description,
    long_description=readme,
    author='Christoph Gohlke',
    author_email='cgohlke@uci.edu',
    url='https://www.lfd.uci.edu/~gohlke/',
    python_requires='>=2.7',
    install_requires=['numpy>=1.14'],
    tests_require=['pytest', 'zstd', 'lz4', 'python-lzf'],
    packages=['imagecodecs'],
    package_data={'imagecodecs': ['licenses/*']},
    license='BSD',
    zip_safe=False,
    platforms=['any'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: BSD License',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: C',
        'Programming Language :: Cython',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        ],
    )

try:
    if '--universal' in sys.argv:
        raise ValueError(
            'Not building the _imagecodecs Cython extension in universal mode')
    setup(ext_modules=ext_modules,
          cmdclass={'build_ext': build_ext},
          **setup_args)
except BaseException as e:
    sep = '\n\n%s\n\n' % ('*' * 80)
    warnings.warn(str(e))
    warnings.warn("""

*******************************************************************

The _imagecodecs Cython extension module was not built.
Using a fallback module with limited functionality and performance.

*******************************************************************
        """)
    setup(**setup_args)
