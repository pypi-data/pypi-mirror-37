import os
import sys

VERSION = '1.0.3'

TAG = os.environ.get("XVECTOR_CLI_RELEASE_TAG")
if TAG is not None and VERSION != TAG:
    info = "Git tag: {0} does not match the version of this app: {1}".format(
        TAG, VERSION
    )
    sys.exit(info)

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

with open('LONG_DESCRIPTION.rst') as f:
    long_description = f.read()

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'xvector'))

install_requires = [
    'requests==2.19.1',
    'pandas==0.23.4'
]

installs_for_two = [
    'pyOpenSSL',
    'ndg-httpsclient',
    'pyasn1'
]

if sys.version_info[0] < 3:
    install_requires += installs_for_two

packages = [
    'xvector'
]

setup(
    name='XVector',
    description='Package for XVector API access',
    keywords=['XVECTOR', 'API', 'data'],
    long_description=long_description,
    version=VERSION,
    author='XVector Labs',
    author_email='hemant.nadakuditi@xvectorlabs.com',
    maintainer='XVector Development Team',
    maintainer_email='hemant.nadakuditi@xvectorlabs.com',
    url='https://gitlab.com/xvectorlabs/pythoncli',
    license='',
    install_requires=install_requires,
    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,test]
    extras_require={
        'dev': [],
        'test': [],
    },
    packages=find_packages(exclude=['contrib', 'docs', 'test*'])
)
