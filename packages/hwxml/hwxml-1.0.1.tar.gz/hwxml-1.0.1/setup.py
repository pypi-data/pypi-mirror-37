from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='hwxml',
    version='1.0.1',

    description='Parse Happy Wheels XML',
    long_description=long_description,
    long_description_content_type='text/markdown',

    url='https://github.com/kittenswolf/hwxml',
    author='kittenswolf',

    packages=find_packages(),
    install_requires=['beautifulsoup4 == 4.6.0'],
    project_urls={
        'Bug Reports': 'https://github.com/kittenswolf/hwxml/issues',
        'Source': 'https://github.com/kittenswolf/hwxml/'
    },
)