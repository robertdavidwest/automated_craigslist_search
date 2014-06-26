#!/usr/bin/env python
# encoding: utf-8

from distutils.core import setup

setup(name='automated_craigslist_search',
	  version='0.0.1',
	  description='Search craigslist and store the results in pandas dataframe, maybe also convert back to html and send out in an e-mail, eventually to be used to send e-mail alerts when search results change',
	  author='Robert D. West',
	  author_email='robert.david.west@gmail.com',
	  url='https://github.com/robertdavidwest/automated_craigslist_search',
	  packages=['automated_craigslist_search'])