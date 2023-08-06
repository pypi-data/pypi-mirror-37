from os import path
from setuptools import setup, find_packages

VERSION = '0.7'


directory = path.dirname(path.abspath(__file__))
with open(path.join(directory, 'requirements.txt')) as f:
    required = f.read().splitlines()


setup(
    name='bgpack',
    version=VERSION,
    description='BBGLab tool',
    packages=find_packages(),
    install_requires=required,
    entry_points={
            'console_scripts': [
                'bgpack = bgpack.cli:cli'
            ]
        }
)