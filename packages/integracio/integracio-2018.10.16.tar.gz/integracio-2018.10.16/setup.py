#!/usr/bin/env python
# -*- coding: utf-8 -*-

import platform
from setuptools import setup, Extension


if platform.system() == 'Windows':
    switch = '/'
    optim = 'O2'
else:
    switch = '-'
    optim = 'O3'


setup(
    name='integracio',
    version='2018.10.16',
    description='pyFAI on steroids',
    author='Vadim Dyadkin',
    author_email='dyadkin@gmail.com',
    url='https://hg.3lp.cx/integracio',
    license='GPLv3',
    install_requires=[
        'numpy>=1.9',
    ],
    packages=[
        'integracio',
    ],
    ext_modules=[
        Extension(
            'integracio._cgracio_f', [
                'src/cgraciomodule.c',
                'src/splitbbox.c',
                'src/twoth.c',
            ],
            extra_compile_args=[
                f'{switch}{optim}',
                f'{switch}DUSE_FLOATS'
            ],
        ),
        Extension(
            'integracio._cgracio_d', [
                'src/cgraciomodule.c',
                'src/splitbbox.c',
                'src/twoth.c',
            ],
            extra_compile_args=[
                f'{switch}{optim}',
                f'{switch}DUSE_DOUBLES'
            ],
        )
    ],
)
