from setuptools import setup, find_packages

setup(
    name='image_builder',
    version='0.1.1rc0',
    packages=find_packages(),
    install_requires=[
        'shortesttrack-tools==0.1.0rc3',
    ]
)
