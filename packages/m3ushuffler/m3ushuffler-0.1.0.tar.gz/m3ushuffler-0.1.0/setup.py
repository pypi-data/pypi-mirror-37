#!/usr/bin/env python3
import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='m3ushuffler',
    version='0.1.0',
    author='Jan Holthuis',
    author_email='holthuis.jan@googlemail.com',
    description='Shuffle M3U playlists easily',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Holzhaus/m3ushuffler',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    entry_points={
        'console_scripts': [
            'm3ushuffler = m3ushuffler:main',
        ],
    }
)
