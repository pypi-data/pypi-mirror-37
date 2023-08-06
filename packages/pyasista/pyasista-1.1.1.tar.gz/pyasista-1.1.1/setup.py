# -*- coding: utf-8 -*-
import os
import setuptools


here = os.path.abspath(os.path.dirname(__file__))

with open('README.md', 'r', encoding='utf-8') as readme_file:
    readme = readme_file.read()

with open('HISTORY.md', 'r', encoding='utf-8') as history_file:
    history = history_file.read()

long_description = readme + '\n\n' + history

about = {}
with open(os.path.join(here, 'pyasista', '__version__.py'), 'r',
          encoding='utf-8') as about_file:
    exec(about_file.read(), about)

packages = ['pyasista']

setuptools.setup(
    name=about['__title__'],
    version=about['__version__'],
    author=about['__author__'],
    description=about['__description__'],
    long_description=long_description,
    long_description_content_type='text/markdown',
    url=about['__url__'],
    packages=packages,
    license=about['__license__'],
    python_requires='>=3.4',
    classifiers=(
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers'
    ),
)
