__author__ = 'gchlebus'

from setuptools import setup, find_packages

setup(
  name='devtip', # under this name the package will be importable
  version='0.1.0',
  author='Grzegorz Chlebus',
  url='',
  license='BSD 3-Clause',
  author_email='grzegorz.chlebus@mevis.fraunhofer.de',
  description=('Very helpful functions.'),
  long_description='Very helpful functions like add.',
  keywords='foo add',
  packages=find_packages(exclude=['test']),
  classifiers=[
    'Development Status :: 4 - Beta',
    'Topic :: Utilities',
    'Programming Language :: Python',
    'License :: OSI Approved :: BSD License'
  ]
)


# USE