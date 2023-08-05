#!/usr/bin/env python

from distutils.core import setup

setup(name='ybc_switch',
      version='1.0.2',
      description='Switch audio files.',
      long_description='Switch audio files.',
      author='hurs',
      author_email='hurs@fenbi.com',
      keywords=['python', 'switch', 'audio'],
      url='http://pip.zhenguanyu.com/',
      packages=['ybc_switch'],
      package_data={'ybc_coordinate': ['*.py', '1.mp3', 'tmp.wav']},
      license='MIT',
      install_requires=['pydub']
     )