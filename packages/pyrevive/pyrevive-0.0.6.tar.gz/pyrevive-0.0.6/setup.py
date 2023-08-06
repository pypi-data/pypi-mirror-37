from setuptools import setup

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='pyrevive',
    version='0.0.6',
    description='Revive Hardware Restarter API Library',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/RevolutionRigs/pyrevive',
    author='Revolution Rigs',
    author_email='nathan@revolutionrigs.com',
    license='GNU v3.0',
    packages=[ 'pyrevive' ],
    install_requires=[ 'requests' ],
    zip_safe=False)
