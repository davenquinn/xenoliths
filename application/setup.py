import os
from setuptools import setup, find_packages

install_requires = [
    'numpy',
    'scipy',
    'sqlalchemy',
    'geoalchemy2',
    'flask'
    ]

setup(
    name="Xenoliths",
    install_requires=install_requires,
    packages=find_packages(),
)
