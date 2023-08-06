import os
import json
from pathlib import Path
from setuptools import setup, find_packages


VERSION_FILE_NAME = 'version.json'


def read(fname):
    """ Returns the contents of the fname file """
    with open(os.path.join(os.path.dirname(__file__), fname), 'r') as file:
        return file.read()


def get_version():
    """ Reads the version from 'version.json' file. Raises an error if not found. """
    with Path(VERSION_FILE_NAME).open('r') as version_file:
        version = json.load(version_file)
        return version.get('version')


# Available classifiers: https://pypi.org/pypi?%3Aaction=list_classifiers
CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: Apache Software License',
    'Topic :: Office/Business :: Office Suites',
    'Topic :: Software Development :: Libraries',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3 :: Only',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Operating System :: OS Independent',
]


requires = [
    'requests>=2.0.0',
    'requests_oauthlib>=1.0.0',
    'python-dateutil>=2.7',
    'pytz>=2018.5',
    'tzlocal>=1.5.0',
    'beautifulsoup4>=4.0.0',
    'stringcase>=1.2.0'
]

setup(
    name='pyo365',
    version=get_version(),
    packages=find_packages(),
    url=' https://github.com/janscas/pyo365',
    license='Apache License 2.0',
    author='Janscas',
    author_email='janscas@users.noreply.github.com',
    maintainer='Janscas',
    maintainer_email='janscas@users.noreply.github.com',
    description='A simple python library to interact with Microsoft Graph and Office 365 API',
    long_description=read('README.md'),
    long_description_content_type="text/markdown",
    classifiers=CLASSIFIERS,
    python_requires=">=3.4",
    install_requires=requires,
)
