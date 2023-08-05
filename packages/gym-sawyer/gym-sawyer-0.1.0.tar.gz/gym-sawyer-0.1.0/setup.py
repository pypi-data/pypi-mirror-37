from setuptools import find_packages
from setuptools import setup

setup(
    name='gym-sawyer',
    packages=[
        package for package in find_packages() if package.startswith('garage')
    ],
    version='0.1.0',
)
