# -*- coding: utf-8 -*-
"""
Created on Mon Oct 15 16:05:05 2018

@author: wmy
"""

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="wmylxmj",
    version="0.0.4",
    author="wmy",
    author_email="1397322329@qq.com",
    description="bilibili spider",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords = ('wmylxmj', 'webspider'),
    url="https://github.com/wmylxmj/My-Python-Package",
    packages=setuptools.find_packages(),
    classifiers=["Programming Language :: Python :: 3",
                 "License :: OSI Approved :: MIT License",
                 "Operating System :: OS Independent",],
    install_requires=['matplotlib',
                      'selenium',
                      'numpy',
                      'bs4'],
)