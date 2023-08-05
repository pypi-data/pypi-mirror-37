from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='myfunniest',
      version='0.12',
      description='The funniest joke in the world,this is new test',
      url='http://github.com/storborg/funniest',
      author='liguilin',
      author_email='liguilin@zhongan.com',
      long_description=long_description,
      license='MIT',
      packages=['myfunniest'],
      zip_safe=False)
