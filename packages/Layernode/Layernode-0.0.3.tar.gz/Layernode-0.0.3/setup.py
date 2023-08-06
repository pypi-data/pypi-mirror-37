#!/usr/bin/env python
from distutils.core import setup

from setuptools import find_packages


def readme():
    with open('README.md') as f:
        return f.read()


setup(
    name='Layernode',
    version='0.0.3',
    description='LayerProtocol blockchain',
    long_description=readme(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
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
