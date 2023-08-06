"""
Basic setup.py file
"""

from setuptools import setup, find_packages

setup(
    name='oows',
    version='0.0.4',
    author='Felipe "Bidu" Rodrigues',
    author_email='felipe@felipevr.com',
    packages=find_packages(),
    url='',
    license='LICENSE.md',
    description=' An object-oriented friendly & pythonic client for Amazon Web Services (AWS)',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=[
        "boto3 == 1.7.80",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
