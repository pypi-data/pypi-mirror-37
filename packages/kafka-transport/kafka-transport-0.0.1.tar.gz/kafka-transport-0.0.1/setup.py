from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='kafka-transport',
      version='0.0.1',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='http://github.com/storborg/funniest',
      author='Nozdrin-Plotnitsky Nikolay',
      author_email='nozdrin.plotnitsky@gmail.com',
      license='MIT',
      packages=find_packages())
