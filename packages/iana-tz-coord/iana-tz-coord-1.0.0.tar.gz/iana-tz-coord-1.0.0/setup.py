"""Setup for pytest-hammertime plugin."""

from setuptools import find_packages, setup

with open('README.md', 'r') as readme:
    long_description = readme.read()

setup(
    name='iana-tz-coord',
    version='1.0.0',
    description='Get the longitude and latitude of an iana timezone\'s principal location',
    url='https://github.com/zhammer/iana-tz-coord',
    packages=('iana_tz_coord',),
    author='Zach Hammer',
    author_email='zach.the.hammer@gmail.com',
    license='MIT License',
    long_description=long_description,
    long_description_content_type='text/markdown'
)
