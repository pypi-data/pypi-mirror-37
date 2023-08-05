#!/usr/bin/env python

from distutils.core import setup

setup(name='ybc_bot',
      version='1.0.3',
      description='Smart bot. ',
      long_description='Smart bot little ape. ',
      author='hurs',
      author_email='hurs@fenbi.com',
      keywords=['python', 'smart bot', 'bot'],
      url='http://pip.zhenguanyu.com/',
      packages=['ybc_bot'],
      package_data={'ybc_bot': ['*.py']},
      license='MIT',
      install_requires=['requests', 'ybc_config']
      )