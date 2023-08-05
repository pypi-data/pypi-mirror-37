from setuptools import setup
from os import path

# read the contents of the README file
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

__version__ = '1.0.0'

setup(
    name='mothership-client',
    version=__version__,
    author='Mothership',
    author_email='dev@spicket.io',
    packages=['mothership',],
    license='MIT',
    description='The official Mothership configuration client for Python',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/spicket/mothership-client-python',
    download_url="https://github.com/spicket/mothership-client-python/tarball/" + __version__,
    install_requires=[
        'requests'
    ]
)