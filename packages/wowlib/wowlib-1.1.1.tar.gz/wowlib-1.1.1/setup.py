# coding:utf-8

from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
	name='wowlib',
	version='1.1.1',
	description='Excel convert tools for wow group',	
	long_description=long_description,
	long_description_content_type="text/markdown",
	author='peakgao',
	author_email='peakgao163@163.com',
	license="MIT",
	url='https://www.q1.com',
	packages=['wowlib'],
	#packages=setuptools.find_packages(),
	install_requires=[
        "xlrd",
        ],	
	classifiers=[
	    "Programming Language :: Python :: 3",
	    "License :: OSI Approved :: MIT License",
	    "Operating System :: OS Independent",
	],
)