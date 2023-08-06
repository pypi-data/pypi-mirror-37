from setuptools import setup, find_packages
setup(
  name = 'fhirtools',
  version='0.0.2',
  description = 'FHIR tools for python.',
  author = 'Jorge Sancho',
  author_email = 'jslarraz@gmail.com',
  url = 'https://github.com/jslarraz/fhirtools', # use the URL to the github repo

  packages=find_packages(),
  package_data={
    '': ['schemas/*.schema.json'],
  },
  include_package_data=True,
  install_requires=[
    'requests', 'jsonschema',
  ],

  #download_url = 'https://github.com/jslarraz/fhirtools/tarball/0.1',
  keywords = ['fhir', 'development'],
  classifiers = [],
)
