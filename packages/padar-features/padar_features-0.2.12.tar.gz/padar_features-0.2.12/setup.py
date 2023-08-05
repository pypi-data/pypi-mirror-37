from setuptools import setup, find_packages

setup(
    name='padar_features',
    version='0.2.12',
    packages=find_packages(),
    include_package_data=True,
    description='Extension of feature computation to be used in padar package',
    long_description=open('README.md').read(),
    install_requires=[
        "pandas>=0.23.0",
        "numpy>=1.15.1",
        "scipy>=1.1.0",
        "dask[complete]>=0.18.1",
        "bokeh>=0.13.0",
        "padar_parallel>=0.2.5",
        "padar_converter>=0.2.17"
    ],
)