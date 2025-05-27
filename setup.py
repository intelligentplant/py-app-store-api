from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
   name='intelligent_plant',
   url="https://github.com/intelligentplant/py-app-store-api",
   version='1.8.1',
   description='A wrapper for the Intelligent Plant data API',
   long_description=long_description,
   long_description_content_type="text/markdown",
   author='Intelligent Plant',
   author_email="support@intelligentplant.com",
   packages=['intelligent_plant'],
   install_requires=['requests', 'pandas']
)
