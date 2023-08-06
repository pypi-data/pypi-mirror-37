from setuptools import setup

from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='datanab',
      version='0.0.2',
      description='A Python wrapper around the datanab API',
      long_description=long_description,
      url='https://github.com/jmfernandes/datanab',
      author='Josh Fernandes',
      author_email='joshfernandes@mac.com',
      keywords=['datanab'],
      license='MIT',
      python_requires='>=3',
      packages=['datanab'],
      requires=['requests'],
      install_requires=[
          'requests',
      ],
      test_suite='nose.collector',
      tests_require=['nose'],
      zip_safe=False)
