# coding: utf-8
import os
import sys
from setuptools import setup, find_packages

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
assert os.path.join(os.path.dirname(__file__), 'src') in sys.path, "Diretório 'src' não consta no PYTHONPATH"

#print(sys.path)
#print(os.environ)
#print(os.environ.get('PYTHONPATH'))
#print(os.environ.get('PATH'))


NAME = 'incolumepy.saj_projects'
NAMESPACE = NAME.split('.')[:-1]
DESCRIPTION = "package incolumepy saj"
KEYWORDS = 'python incolumepy saj'
AUTHOR = '@britodfbr'
AUTHOR_EMAIL = 'contato@incolume.com.br'
URL = 'https://gitlab.com/development-incolume/saj_projects/'
PROJECT_URLS = {
    'Documentation': 'https://gitlab.com/development-incolume/saj_projects/',
    'Funding': None,
    'Say Thanks!': None,
    'Source': 'https://gitlab.com/development-incolume/saj_projects',
    'Git': 'https://gitlab.com/development-incolume/saj_projects.git',
    'Tracker': 'https://gitlab.com/development-incolume/saj_projects/issues',
    'Oficial': '',
}
LICENSE = 'BSD'

# Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
CLASSIFIERS = [
    # 'Development Status :: 5 - Production/Stable',
    'Development Status :: 4 - Beta',
    'Operating System :: OS Independent',
    'Natural Language :: Portuguese (Brazilian)',
    "Programming Language :: Python",
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Topic :: Utilities']

VERSION = open(os.path.join('src', \
NAME.replace('.','/'), "version.txt")).read().strip()

# VERSION = __import__(NAME).__version__

with open('README.md') as f:
    readme = f.read()
with open(os.path.join('docs', 'HISTORY.rst')) as f:
    history = f.read()
with open(os.path.join('docs', 'EXAMPLES.rst')) as f:
    examples = f.read()
with open(os.path.join('docs', 'CONTRIBUTORS.rst')) as f:
    contributors = f.read()
with open(os.path.join('docs', 'CHANGES.rst')) as f:
    changes = f.read()

# LONG_DESCRIPTION = ('{}\n\n{}\n\n{}\n\n{}\n\n{}\n'.format(readme, history, examples, contributors, changes))
LONG_DESCRIPTION = '\n\n'.join((readme, history, examples, contributors, changes))


setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    classifiers=CLASSIFIERS,
    keywords=KEYWORDS,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    project_urls=PROJECT_URLS,
    license=LICENSE,
    namespace_packages=NAMESPACE,
    packages=find_packages('src', exclude=['ez_setup', 'examples', 'tests', 'exemplos', 'view']),
    package_dir={'': 'src'},
    test_suite='nose.collector',
    tests_require='nose',
    zip_safe=False,
    install_requires=[
        'setuptools',
        # -*- Extra requirements: -*-
        'pytest',
        'nose',
        'deprecated',
        'incolumepy.utils>=0.7',
        'pandas',
        'bs4',
        'lxml',
        'html5lib'
    ],
    entry_points={
        'console_scripts': [
            'fs_report = incolumepy.saj_projects.fs_report:run',
            'fsreport = incolumepy.saj_projects.fs_report:run',
            'interval = incolumepy.checkinterval.Check:Check.interval'
        ],
        'gui_scripts': [
            'baz = my_package_gui:start_func',
        ],
    },
    # -*-Data files-*-
    include_package_data=True,
    exclude_package_data={'': ['saj_projects']},
    package_data={
        # If any package contains *.txt or *.rst files, include them:
        # '': ['*.txt', '*.rst'],
        # And include any *.msg files found in the 'hello' package, too:
        'data': ['data/*.cvs', 'data/*.xlsx'],
        'drivers': ['drivers/*']
    },
    dependency_links=[
        # "http://peak.telecommunity.com/snapshots/"
    ],
    # entry_points="""
    # -*- Entry points: -*-

    # [distutils.setup_keywords]
    # paster_plugins = setuptools.dist:assert_string_list
    # [egg_info.writers]
    # paster_plugins.txt = setuptools.command.egg_info:write_arg
    # """,
    # paster_plugins = [''],
)
