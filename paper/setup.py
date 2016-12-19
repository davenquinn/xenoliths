import os
from setuptools import setup, find_packages

install_requires = [
    'xenoliths'
    ]

setup(
    name="paper",
    install_requires=install_requires,
    packages=find_packages(),
    package_dir=dict(paper="paper"),
    entry_points='''
        [console_scripts]
        paper=paper:cli
    ''')
