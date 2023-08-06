import codecs
import os
import sys

try:
	from setuptools import setup
except:
	from distutils.core import setup



def read(fname):
	return codecs.open(os.path.join(os.path.dirname(__file__), fname)).read()

platforms = ['linux/Windows']
classifiers = [
    'Development Status :: 3 - Alpha',
    'Topic :: Text Processing',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.5',
]

install_requires = [
]

    
setup(name='xmail',
      version='0.0.14',
      description='A simple send mail package',
      py_modules=['xmail/xmail', 'xmail/__init__'],
      author = "Jianglong",  
      author_email = "592519397@qq.com" ,
      url = "https://jlong0104.github.io" ,
      license="Apache License, Version 2.0",
      platforms=platforms,
      classifiers=classifiers,
      install_requires=install_requires     
      )   
