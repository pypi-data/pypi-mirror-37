from setuptools import setup, find_packages
import sys, os

version = '1.0.4'

setup(name='yaml-config-parser',
      version=version,
      description="A simple yaml config parser tool",
      long_description="""\
A simple yaml config parser tool""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='yaml config parser',
      author='luserv',
      author_email='vasterlu@gmail.com',
      url='https://github.com/luserv/yaml-config-parser',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          "pyyaml"
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
