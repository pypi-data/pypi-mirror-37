#!/usr/bin/env python

from distutils.core import setup

setup(name='ybc_idiom',
      version='1.0.8',
      description='Get The idiom info.',
      long_description='Get The idiom info',
      author='hurs',
      author_email='hurs@fenbi.com',
      keywords=['python', 'idiom', 'search'],
      url='http://pip.zhenguanyu.com/',
      packages=['ybc_idiom'],
      package_data={'ybc_idiom': ['idioms.txt', '*.py']},
      license='MIT',
      install_requires=['requests', 'ybc_config']
      )