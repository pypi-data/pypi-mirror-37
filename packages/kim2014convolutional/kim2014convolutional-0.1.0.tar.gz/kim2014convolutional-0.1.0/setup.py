# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

def long_description(filename):
    with open(filename, mode='r') as fd:
        return fd.read()

setup(name='kim2014convolutional',
      version='0.1.0',

      description='Implementation of kim2014convolutional',
      long_description=long_description('README.md'),
      long_description_content_type='text/markdown',

      url='https://github.com/wnohang/kim2014convolutional',
      project_urls={
          'Source': 'https://github.com/wnohang/kim2014convolutional',
          'Issues': 'https://github.com/wnohang/kim2014convolutional/issues',
      },

      classifiers=[
          'Development Status :: 1 - Planning',
          'Intended Audience :: Developers',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.6',
          'Topic :: Education',
          'Topic :: Scientific/Engineering :: Artificial Intelligence'
      ],
      keywords='research model',

      license='MIT',
      author='Cesar Perez',
      author_email='cperez@wnohang.com',

      packages=find_packages(),
      install_requires=[
          'keras'
      ],

      include_package_data=True,
      zip_safe=True)
