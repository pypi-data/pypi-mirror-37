# -*- coding: utf-8 -*-

import codecs
import os
import re
import sys

from setuptools import find_packages, setup

# base_dir = os.path.dirname(__file__)

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

name = 'django-datatables-too'
package = 'django_datatables_too'
description = 'Django integration with jQuery DataTables.'
url = 'https://bitbucket.org/tsantor/django-datatables-too'
author = 'Tim Santor'
author_email = 'tsantor@xstudios.agency'
license = 'MIT'
install_requires = [

]
classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3.6',
]

def get_version(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    init_py = codecs.open(os.path.join(package, '__init__.py'), encoding='utf-8').read()
    return re.search("^__version__ = ['\"]([^'\"]+)['\"]", init_py, re.MULTILINE).group(1)

if sys.argv[-1] == 'build':
    os.system("python setup.py sdist bdist_wheel")

if sys.argv[-1] == 'publish':
    os.system("python setup.py sdist upload")
    args = {'version': get_version(package)}
    print("You probably want to also tag the version now:")
    print("    git tag -a %(version)s -m 'version %(version)s' && git push --tags" % args)
    sys.exit()

EXCLUDE_FROM_PACKAGES = []

setup(name=name,
    version=get_version(package),
    description=description,
    long_description=readme + '\n\n' + history,
    url=url,
    author=author,
    author_email=author_email,
    license=license,
    packages=find_packages(exclude=EXCLUDE_FROM_PACKAGES),
    install_requires=install_requires,
    classifiers=classifiers,
    zip_safe=False)
