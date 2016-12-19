import os
from setuptools import setup, find_packages

setup(
    name="paper",
    packages=find_packages(),
    package_dir=dict(paper="paper"),
    entry_points='''
        [console_scripts]
        paper=paper:cli
    ''')
