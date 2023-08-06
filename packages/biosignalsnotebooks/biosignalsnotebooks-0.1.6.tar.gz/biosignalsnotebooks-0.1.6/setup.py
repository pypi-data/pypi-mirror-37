"""
File that specifies package requisites for a correct functioning of all available functions.

"""

from setuptools import setup
from os import path

# read the contents of your README file
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README_BSN.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(name='biosignalsnotebooks',
      version='0.1.6',
      description='A Python package for supporting the external loading and processing of '
                  'OpenSignals electrophysiological acquisitions.',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://github.com/biosignalsnotebooks/biosignalsnotebooks',
      author='Plux Wireless Biosignals',
      author_email='gramos@plux.info',
      license='MIT',
      packages=['biosignalsnotebooks'],
      install_requires=[
          'numpy', 'pylab', 'scipy', 'h5py', 'pyedflib', 'python-magic', 'wget', 'datetime',
          'libmagic', 'bokeh', 'scipy', 'IPython', 'pandas', 'novainstrumentation', 'importlib',
          'nbformat'
      ],
      zip_safe=False,
      include_package_data=True)

# 11/10/2018 16h45m :)
