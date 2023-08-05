#!/usr/bin/env python

from distutils.core import setup

setup(name='ybc_imgcar',
      version='1.0.4',
      description='Recognition Image Car Brand',
      long_description='Recognition Image Car Brand',
      author='hurs',
      author_email='hurs@fenbi.com',
      keywords=['python', 'car', 'recognition'],
      url='http://pip.zhenguanyu.com/',
      packages=['ybc_imgcar'],
      package_data={'ybc_imgcar': ['test.jpg', '*.py']},
      license='MIT',
      install_requires=['requests', 'ybc_config']
      )