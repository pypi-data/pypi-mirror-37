#!/usr/bin/env python

from distutils.core import setup

setup(name='ybc_wordcloud',
      version='1.0.4',
      description='Generate wordcloud.',
      long_description='Generate text wordcloud according word frequency.',
      author='hurs',
      author_email='hurs@fenbi.com',
      keywords=['python', 'wordcloud', 'text wordcloud'],
      url='http://pip.zhenguanyu.com/',
      packages=['ybc_wordcloud'],
      package_data={'ybc_wordcloud': ['*.py']},
      license='MIT',
      install_requires=['wordcloud', 'jieba', 'imageio']
      )