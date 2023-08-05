# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import io
import os
import re


def read(*names, **kwargs):
    with io.open(
        os.path.join(os.path.dirname(__file__), *names),
        encoding=kwargs.get("encoding", "utf8")
    ) as fp:
        return fp.read()


long_description = read('README.rst')


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setup(name='elampclient',
      version=find_version('elampclient', 'version.py'),
      description='eLamp API clients for Web API',
      long_description=long_description,
      url='https://github.com/elampapi/python-elampclient',
      author='eLamp',
      author_email='support@elamp.fr',
      license='MIT',
      classifiers=[
            'Development Status :: 5 - Production/Stable',
            'Intended Audience :: Developers',
            'Topic :: System :: Networking',
            'Topic :: Office/Business',
            'Programming Language :: Python :: 2',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.3',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
      ],
      keywords='elamp elamp-web elamp-api skill skill data',
      packages=find_packages(exclude=['docs', 'docs-src', 'tests']),
      install_requires=[
          'websocket-client >=0.35, <1.0a0',
          'requests >=2.11, <3.0a0',
          'six >=1.10, <2.0a0',
          'PyJWT >=1.6.4',
          'cryptography >=2.3'
      ])