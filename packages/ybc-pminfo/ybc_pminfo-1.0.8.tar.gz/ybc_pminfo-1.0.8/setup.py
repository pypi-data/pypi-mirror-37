#!/usr/bin/env python

from distutils.core import setup

setup(name='ybc_pminfo',
      version='1.0.8',
      description='Get The PM2.5 Info.',
      long_description='Get The PM2.5 Info.',
      author='hurs',
      author_email='hurs@fenbi.com',
      keywords=['python', 'pm', 'pm2.5'],
      url='http://pip.zhenguanyu.com/',
      packages=['ybc_pminfo'],
      package_data={'ybc_pminfo': ['*.py']},
      license='MIT',
      install_requires=['requests', 'ybc_config']
      )