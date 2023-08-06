#!/usr/bin/env python

from distutils.core import setup

setup(name='ybc_scene',
      version='1.0.4',
      description='Scene Object Recognition.',
      long_description='Scene Object Recognition.',
      author='hurs',
      author_email='hurs@fenbi.com',
      keywords=['python', 'object', 'scene', 'recognition'],
      url='http://pip.zhenguanyu.com/',
      packages=['ybc_scene'],
      package_data={'ybc_scene': ['*.py']},
      license='MIT',
      install_requires=['requests', 'ybc_config']
      )