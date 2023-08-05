"""
setup.py for oas3
"""

__author__ = "Pinn Technologies, Inc."
__email__ = "developers@pinn.ai"
__copyright__ = "Copyright 2018, Pinn Technologies, Inc."

import os
from setuptools import setup, find_packages

this_dir = os.path.abspath(os.path.dirname(__file__))
REQUIREMENTS = filter(None, open(
    os.path.join(this_dir, 'requirements', 'main.txt')).read().splitlines())

import versioneer

setup(
    name='wsh',
    author=__author__,
    author_email=__email__,
    license="MIT",
    url="https://wsh.readthedocs.org",
    zip_safe=False,
    scripts=['bin/wsh'],
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    install_requires=list(REQUIREMENTS),
    classifiers=[k for k in open('CLASSIFIERS').read().split('\n') if k],
    description='An interactive WebSocket shell',
    long_description=open('README.rst').read() + open('HISTORY.rst').read(),
    packages=find_packages(exclude=["tests*"])
)
