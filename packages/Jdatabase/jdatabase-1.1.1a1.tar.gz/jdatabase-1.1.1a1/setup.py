from setuptools import setup, find_packages

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='jdatabase',
      version='1.1.1-alpha1',
      packages=['jdatabase'],
      license='MIT',
      description='jdatabase Python package, designed for ease of database control and interaction within Python. The jdatabase package supports MySQL and PostgreSQL database systems.',
      long_description=long_description,
      long_description_content_type='text/markdown',
      install_requires=['mysqlclient', 'psycopg2-binary'],
      url='https://github.com/JoshWidrick/jdatabase',
      author='Joshua Widrick',
      author_email='jjwidric@buffalo.edu',
)

"""
python setup.py sdist
twine upload --repository pypi dist/*
"""