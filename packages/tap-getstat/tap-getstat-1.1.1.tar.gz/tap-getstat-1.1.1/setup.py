#!/usr/bin/env python

from setuptools import setup

setup(name='tap-getstat',
      version='1.1.1',
      description='Singer.io tap for extracting data from the getstat.com API',
      author='Nick Hassell',
      url='https://singer.io',
      classifiers=['Programming Language :: Python :: 3 :: Only'],
      py_modules=['tap_getstat'],
      install_requires=[
          'singer-python',
          'requests',
          'backoff==1.3.2'
      ],
      entry_points='''
          [console_scripts]
          tap-getstat=tap_getstat:main
      ''',
      packages=['tap_getstat'],
      package_data = {
          'tap_getstat/schemas': [
            "projects.json",
            "sites.json",
            "tags.json",
            "keywords.json",
            "rankings.json",
						"sov.json"
          ],
      },
      include_package_data=True,
)
