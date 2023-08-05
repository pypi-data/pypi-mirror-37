#!/usr/bin/env python

from distutils.core import setup

setup(name='ybc_namecard',
      version='1.0.5',
      description='Recognize Name Card By Ocr',
      long_description='Recognize Name Card By Ocr',
      author='hurs',
      author_email='hurs@fenbi.com',
      keywords=['python', 'namecard', 'ocr'],
      url='http://pip.zhenguanyu.com/',
      packages=['ybc_namecard'],
      package_data={'ybc_namecard': ['test.jpg', '*.py']},
      license='MIT',
      install_requires=['requests', 'ybc_config']
      )