from setuptools import setup, find_packages

setup(
    name="heatflow",
    version="1.0.0",
    long_description=__doc__,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    entry_points='''
        [console_scripts]
        heatflow=heatflow.manage:cli
    '''
)
