from setuptools import setup
from setuptools import find_packages
from os import path

# read the contents of your README file
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
  name = 'targomo_python',
  long_description=long_description,
  long_description_content_type='text/markdown',
  packages = find_packages(),
  version = '0.23',
  description = 'A python client library to query the Targomo API',
  author = 'Targomo GmbH',
  author_email = 'mail@targomo.com',
  url = 'https://github.com/targomo/targomo-python',
  download_url = 'https://github.com/targomo/targomo-python/tarball/0.23',
  install_requires=[
     'requests',
 ],
  keywords = ['isochrone', 'routing', 'polygon', 'openstreetmaps', 'gtfs', 'map'],
  classifiers = [],
)
