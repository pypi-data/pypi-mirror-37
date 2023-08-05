#!/usr/bin/env python

from distutils.core import setup

setup(name='ybc_trans',
      version='1.0.4',
      description='Translate dictionary.',
      long_description='Translate dictionary zh to en ,en to zh.',
      author='hurs',
      author_email='hurs@fenbi.com',
      keywords=['python', 'trans', 'translate'],
      url='http://pip.zhenguanyu.com/',
      packages=['ybc_trans'],
      package_data={'ybc_trans': ['*.py']},
      license='MIT',
      requires=['ybc_config', 'requests']
     )