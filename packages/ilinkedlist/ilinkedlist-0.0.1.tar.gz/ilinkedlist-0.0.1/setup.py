#!/usr/bin/python3.6

import setuptools

setuptools.setup(
  name='ilinkedlist',
  version='0.0.1',
  description='An immutable linked list library.',
  long_description='This is an implementation of immutable linked lists. It contains `nil` (the empty linked list) and a `Pair` class for nodes.',
  url='https://github.com/luther9/ilinkedlist-py',
  author='Luther Thompson',
  author_email='lutheroto@gmail.com',
  license='GPLv3+',
  classifiers=[
    'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
    'Programming Language :: Python :: 3.6',
    'Development Status :: 4 - Beta',
  ],
  python_requires='~= 3.6',

  # WARNING: This parameter is undocumented, but it's the only way I can get
  # the module to install properly. Note that the 'packages' parameter only
  # works for packages, not modules.
  py_modules=('ilinkedlist',),
)
