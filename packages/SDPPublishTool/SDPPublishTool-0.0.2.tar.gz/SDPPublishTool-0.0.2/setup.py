#!/usr/bin/env python
#-*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: tanzou
# Mail: 'tanzou34@gmail.com'
# Created Time:  2018-10-10 19:17:34
#############################################


from setuptools import setup, find_packages


setup(
      name='SDPPublishTool',
      version = "0.0.2",
      keywords = ("pip", "SDP"),
      description = "SDP publish",
      long_description = "SDP publish for NetDragon",
      license = "MIT Licence",
      
      url = "",
      author = "tanzou",
      author_email = "tanzou34@gmail.com",
      
      packages = find_packages(),
      include_package_data = True,
      platforms = "any",
      install_requires = ["splinter", "getpass2"]
)
