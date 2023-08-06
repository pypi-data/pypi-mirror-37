import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

try:
    long_description = open("README.md").read()
except IOError:
    long_description = ""


setup(
    name='text-indexer',
    version='0.0.1',
    description="Yoctol Text Indexer",
    url="https://github.com/Yoctol/text-indexer",
    license="MIT",
    author="Yoctol Info",
    author_email='yien.tsai@yoctol.com',
    packages=find_packages(),
    python_requires='>=3.6',
    install_requires=[
        "strpipe==0.4.7",
        "u-msgpack-python==2.5.0",
    ],
    include_package_data=True,
    long_description=long_description,
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
    ],
)
