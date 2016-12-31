from setuptools import setup, find_packages

install_requires = [
    'numpy',
    'scipy',
    'matplotlib',
    'seaborn',
    'fipy',
    'pint'
    ]

setup(
    name='geotherm',
    version="0.1",
    description="Tools for computing 1d geothermal gradients.",
    license='MIT',
    keywords='geology geophysics data computation science',
    author='Daven Quinn',
    author_email='dev@davenquinn.com',
    maintainer='Daven Quinn',
    maintainer_email='dev@davenquinn.com',
    url='http://github.com/davenquinn/geotherm',
    install_requires=install_requires,
    tests_require=['nose'],
    test_suite='nose.collector',
    packages=find_packages(),
    package_dir={'geotherm':'geotherm'},
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Science/Research',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
)
