from setuptools import setup, find_packages
import sys, os

version = '3.0.4'

with open("README.md","r") as fh:
      long_description=fh.read()



setup(name="njnuko",
      version="3.0.4",
      description="file sorting",
      long_description="file sorting project",
      classifiers=[], 
      keywords='njnuko',
      author='njnuko',
      author_email='njnuko@163.com',
      url='https://github.com/njnuko/njnuko',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=['psycopg2','pymysql'],
      entry_points="",
      py_modules=[],
      )
