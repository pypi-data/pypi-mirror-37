# -*- coding: utf-8 -*-

"""A setuptools-based setup module.

See:
https://github.com/renweizhukov/txt2mobi3_app
"""

from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='txt2mobi3_app',
    version='0.1.0',
    description='A PyQt5 application for converting Chinese novel txt files into Kindle mobi files.',
    long_description=long_description,
    url='https://github.com/renweizhukov/txt2mobi3_app',
    author='Wei Ren',
    author_email='renwei2004@gmail.com',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: End Users/Desktop',
        'Topic :: Text Processing :: General',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        ],
    keywords='txt mobi python3 pyqt5',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'PyQt5',
        'txt2mobi3',
        'setuptools',
        ],
    python_requires='>=3',
    entry_points={
        'console_scripts': [
            'txt2mobi3_app=txt2mobi3_app.txt2mobi3_app:txt2mobi3_app'
        ],
        },
    project_urls={
        'Bug Reports': 'https://github.com/renweizhukov/txt2mobi3_app/issues',
        'Documentation': 'https://github.com/renweizhukov/txt2mobi3_app',
        'Source': 'https://github.com/renweizhukov/txt2mobi3_app',
        },
    )