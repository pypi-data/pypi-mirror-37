#!/usr/bin/env python

from setuptools import setup

# python setup.py sdist

version = '0.0.1'

with open('README.md', 'r') as f:
    readme = f.read()

requirements = [

]

setup(
    name='disorg',
    version=version,
    description='Rapid note and task tracking application.',
    long_description=readme,
    author='Zachary Crites',
    url='https://gitlab.com/zaccrites/disorg',
    packages=[
        'disorg',
    ],
    package_dir={'disorg': 'disorg'},
    entry_points={
        'console_scripts': [
            'disorg = disorg.__main__:main',
        ]
    },
    include_package_data=True,
    python_requires='>=3.6',
    install_requires=requirements,
    license='MIT',
    classifiers=[

    ],
    keywords='',
)
