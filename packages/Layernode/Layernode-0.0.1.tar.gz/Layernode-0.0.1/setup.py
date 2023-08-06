#!/usr/bin/env python
from distutils.core import setup

from setuptools import find_packages

setup(
    name='Layernode',
    version='0.0.1',
    description='LayerProtocol blockchain',
    author='NoRestLabs',
    author_email='galen@norestlabs.com',
    url='https://github.com/LayerProtocol/layernode.git',
    entry_points={
        'console_scripts': [
            'layernode = layernode.cli:main'
        ],
    },
    include_package_data=True,
    install_requires=['altgraph', 'dnspython', 'wheel', 'pyyaml', 'flask', 'flask-socketio', 'm3-cdecimal', 'pyopenssl',
                      'werkzeug', 'tabulate', 'ecdsa', 'plyvel',
                      'layer-py', 'enum-compat', 'eventlet', 'future', 'greenlet', 'ipfsapi', 'macholib', 'pefile',
                      'psutil', 'PyInstaller', 'PyMySQL', 'python-slugify',
                      'requests-toolbelt', 'simplekv', 'SQLAlchemy', 'Unidecode', 'websocket-client'],
    packages=find_packages(exclude=("tests", "tests.*")),
)
