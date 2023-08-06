import os
from incolumepy.utils.utils import  namespace
from setuptools import setup, find_packages
import incolumepy.utils as package

NAME = 'incolumepy.utils'
NAMESPACE = namespace(NAME)
DESCRIPTION = "package incolumepy utils"
KEYWORDS = 'python utils incolumepy'
AUTHOR = '@britodfbr'
AUTHOR_EMAIL = 'contato@incolume.com.br'
URL = 'http://www.incolume.com.br'
PROJECT_URLS={
    'Documentation': 'https://brito.blog.incolume.com.br/search/label/development-incolume',
    'Funding': None,
    'Say Thanks!': None,
    'Source': 'https://gitlab.com/development-incolume/incolumepy.utils',
    'Git': 'https://gitlab.com/development-incolume/incolumepy.utils.git',
    'Tracker': 'https://gitlab.com/development-incolume/incolumepy.utils/issues',
    'Oficial': 'https://pypi.org/project/incolumepy.utils/',
}
LICENSE = 'BSD'
CLASSIFIERS = [
'Development Status :: 5 - Production/Stable',
'Operating System :: OS Independent',
'Natural Language :: Portuguese (Brazilian)',
"Programming Language :: Python",
'Topic :: Software Development :: Libraries :: Python Modules',
'Topic :: Utilities',]

VERSION = package.__version__
LONG_DESCRIPTION = (
        open('README.md').read()
        + '\n\n'
        +'History\n'
        +'=======\n'
        + '\n' +
        open(os.path.join("docs", "HISTORY.rst")).read()
        + '\n\n'
        +'Examples\n'
        +'=======\n'
        +'\n'+
        open(os.path.join('docs', 'EXAMPLES.rst')).read()
        + "\n\n"
        +'Contributors\n'
        +'============\n'
        + '\n' +
        open(os.path.join('docs', 'CONTRIBUTORS.rst')).read()
        + '\n\n'
        +'Changes\n'
        +'=======\n'
        + '\n' +
        open(os.path.join('docs', 'CHANGES.rst')).read()
        + '\n'
)

setup(name=NAME,
      version=VERSION,
      description=DESCRIPTION,
      long_description=LONG_DESCRIPTION,

      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=CLASSIFIERS,
      keywords=KEYWORDS,
      author=AUTHOR,
      author_email=AUTHOR_EMAIL,
      url=URL,
      project_urls= PROJECT_URLS,
      license=LICENSE,
      namespace_packages=NAMESPACE,
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      test_suite='nose.collector',
      tests_require='nose',
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
          'pytest',
          'nose',
          'rstr',
      ],
      entry_points={
          'console_scripts': [
              'checkinterval = incolumepy.checkinterval.Check:Check.main',
              'interval = incolumepy.checkinterval.Check:Check.interval'
          ],
          'gui_scripts': [
              'baz = my_package_gui:start_func',
          ],
      },

      # entry_points="""
      ## -*- Entry points: -*-

      # [distutils.setup_keywords]
      ##paster_plugins = setuptools.dist:assert_string_list

      # [egg_info.writers]
      ##paster_plugins.txt = setuptools.command.egg_info:write_arg
      # """,
      # paster_plugins = [''],
      )
