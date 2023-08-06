try:
    from setuptools import setup
except:
    from distutils.core import setup


setup(
    name='armus',
    packages=['armus'],
    scripts=['bin/create_migration.py'],
    version='0.2.0',
    description='A tool for running migrations',
    author='uStudio',
    author_email='dev@ustudio.com',
    url='https://github.com/ustudio/armus')
