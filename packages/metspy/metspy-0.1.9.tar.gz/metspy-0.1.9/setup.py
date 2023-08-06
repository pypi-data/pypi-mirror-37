#!/usr/bin/env python
#-*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: soonyenju
# Mail: soonyenju@foxmail.com
# Created Time:  2018-10-23 13:28:34
#############################################


from setuptools import setup, find_packages

setup(
	name = "metspy",
	version = "0.1.9",
	keywords = ("pip", "meteorology","scraping", "aqi", "soonyenju"),
	description = "Scraping AQI, PM2.5 and meteorological parameters",
	long_description = "Scraping global in-situ pollutant and meteorology hourly",
	license = "MIT Licence",

	url = "https://github.com/soonyenju/metSpy",
	author = "soonyenju",
	author_email = "soonyenju@foxmail.com",

	packages = find_packages(),
	include_package_data = True,
	platforms = "any",
	install_requires = [
		# "pathlib",
		# "pickle",
		# "pandas",
		# "bs4",
		# "datetime",
		# "requests"
	]
)
