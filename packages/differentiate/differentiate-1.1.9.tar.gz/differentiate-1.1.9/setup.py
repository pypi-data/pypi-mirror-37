import os
from setuptools import setup, find_packages


name = 'differentiate'


def get_version(package_name, version_file='_version.py'):
    """Retrieve the package version from a version file in the package root."""
    filename = os.path.join(os.path.dirname(__file__), package_name, version_file)
    with open(filename, 'rb') as fp:
        return fp.read().decode('utf8').split('=')[1].strip(" \n'")


setup(
    name=name,
    version=get_version(name),
    packages=find_packages(),
    url='https://github.com/mrstephenneal/differentiate',
    entry_points={
        'console_scripts': [
            'differ = differentiate.diff:main'
        ]
    },
    license='MIT License',
    author='Stephen Neal',
    author_email='stephen@stephenneal.net',
    description='Lightweight data differentiator.',
)
