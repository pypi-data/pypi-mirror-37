#!/usr/bin/env python

from distutils.core import setup

setup(name='ybc_box',
      version='3.0.13',
      description='ybc_box provides easy GUI programming.',
      long_description='ybc_box is a module for simple, easy GUI programming in Python',
      author='lijz01',
      author_email='lijz01@fenbi.com',
      keywords=['python', 'box'],
      url='http://pip.zhenguanyu.com/',
      packages=['ybc_box'],
      package_data={'ybc_box': ['__init__.py', 'ybc_box.py', 'boxes/*']},
      license='MIT',
      install_requires=['easygui']
     )