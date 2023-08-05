# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
try:
    long_description = open("README.md").read()
except IOError:
    long_description = ""

setup(
    name="Dataviewer",
    version="0.2.0",
    description="Dataviewer for project files",
    license="MIT",
    author="kdd",
    author_email="kobededecker@gmail.com",
    url="https://gitlab.com/kobededecker/dataviewer",
    packages=find_packages(),
    include_package_data=True,
    scripts=[r'bin\viewer.bat', r'bin\viewer.py'],
    install_requires=['flask', 'flask_cors'],
    long_description=long_description,
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
    ]
)
