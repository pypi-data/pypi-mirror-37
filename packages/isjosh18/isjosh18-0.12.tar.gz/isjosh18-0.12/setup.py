from setuptools import setup

from os import path
import sys

# Open encoding isn't available for Python 2.7 (sigh)
if sys.version_info < (3, 0):
    from io import open 

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='isjosh18',
    packages=['isjosh18'],
    version='0.12',
    author='numirias',
    author_email='numirias@users.noreply.github.com',
    url='https://github.com/numirias/python-isjosh18',
    license='MIT',
    python_requires='>=2.7',
    install_requires=['requests', 'colorama', 'mock'],
    entry_points={
        'console_scripts': [
            'isjosh18 = isjosh18.__main__:main',
        ]
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description='Determines if Josh is 18.',
    long_description=long_description,
    long_description_content_type='text/markdown'
)
