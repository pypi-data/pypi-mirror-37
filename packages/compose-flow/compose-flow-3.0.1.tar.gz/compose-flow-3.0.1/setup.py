#!/usr/bin/env python
from setuptools import find_packages, setup

SRC_PREFIX = 'src'

packages = find_packages(SRC_PREFIX)

def readme():
    with open('README.md') as f:
        return f.read()


setup(
    name='compose-flow',
    url='https://github.com/openslate/compose-flow',
    author='OpenSlate',
    author_email='code@openslate.com',
    version='3.0.1',
    description='codified workflows for docker compose',
    long_description=readme(),
    long_description_content_type='text/markdown',
    package_dir={'':'src'},
    packages=packages,
    entry_points={
        'console_scripts': [
            'compose-flow = compose_flow.entrypoints:compose_flow',
        ],
    },
    install_requires=[
        'PyYAML',
        'boltons',
        'sh',
        'tag-version',
    ]
)
