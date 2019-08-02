from setuptools import setup

setup(
   name='intelligent_plant',
   version='1.1.1',
   description='A wrapper for the Intellinget Plant API',
   author='Intelligent Plant',
   packages=['intelligent_plant'],
   install_requires=['requests', 'pandas']
)