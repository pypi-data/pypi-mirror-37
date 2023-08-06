from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pyprodj',
    version='0.0.1',
    description='Library for interfacing with Pioneer ProDJ Link',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/jackorobot/pyprodj',
    author='Jesse Hoogervorst',
    packages=find_packages(exclude=['docs', 'tests']),
    project_urls={
        'Source': 'https://github.com/jackorobot/pyprodj'
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)