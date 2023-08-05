from setuptools import setup, find_packages
import re

version = ''
with open('dalloriam/__init__.py') as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError('Version is not set')

readme = 'See https://github.com/dalloriam/python-stdlib for README.'

setup(
    name='dalloriam',
    author='William Dussault',
    author_email='dalloriam@gmail.com',
    url='https://github.com/dalloriam/python-stdlib',
    version=version,
    packages=find_packages(),
    license='MIT',
    description='Personal standard library.',
    long_description=readme,
    install_requires=['requests', 'flask']
)