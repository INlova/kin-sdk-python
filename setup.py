#!/usr/bin/env python

from setuptools import setup

exec(open("kin/version.py").read())

with open('requirements.txt') as f:
    requires = [line.strip() for line in f if line.strip()]
with open('requirements-dev.txt') as f:
    tests_requires = [line.strip() for line in f if line.strip()]

setup(
    name='kin-sdk-python',
    version=__version__,
    description='KIN SDK for Python',
    author='Kin Foundation',
    maintainer='David Bolshoy',
    maintainer_email='david.bolshoy@kik.com',
    url='https://github.com/kinfoundation/kin-sdk-python',
    license='GPLv2',
    packages=["kin"],
    long_description=open("README.md").read(),
    keywords = ["kin", "cryptocurrency", "blockchain"],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Development Status :: 4 - Beta',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
    install_requires=requires,
    tests_require=tests_requires,
)
