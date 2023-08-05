from setuptools import setup, find_packages

setup(
    name='image_builder',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'shortesttrack-sdk==1.0.11',
    ]
)
