9# -*- coding: utf-8 -*-
"""
Created on Fri Oct 19 06:12:29 2018

@author: Lenovo
"""

from setuptools import setup,find_packages

setup(name='data_helper_2',
      version='0.2',
      description='A helper containing methods to aid visualisation and preliminary analysis of data',
      url='http://github.com/karthickrajas/data_helper',
      author='Karthick Raja',
      author_email='karthick11b36@gmail.com',
      license='MIT',
      packages=find_packages(),
      install_requires=['sklearn','pandas','matplotlib','seaborn','statsmodels'],
      zip_safe=False)