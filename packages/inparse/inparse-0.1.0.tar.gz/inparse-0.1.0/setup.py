import os
from setuptools import setup

import codecs


def read(fname):
    return codecs.open(os.path.join(os.path.dirname(__file__), fname),encoding="utf-8").read()


setup(name='inparse',
      description='Collaborative AI for  Web Scraping, Data Extraction and Crawling,Knowledge Graph'
                  ' ',
      long_description=read("README.rst"),
      version='0.1.0',
      url='https://github.com/inparse/inparse',
      author='Guojian Li',
      author_email='guojianlee@gmail.com',
      license='BSD',
      python_requires=">=3.6.5",
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: BSD License',
          'Programming Language :: Python :: 3'
      ],
      packages=['inparse'],
      install_requires=[
          'requests',
          'beautifulsoup4',
          'lxml'


      ],

      )
