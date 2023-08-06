import os
from setuptools import setup, find_packages

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
# def read(fname):
#     return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="sendslack",
    version="0.0.1",
    author="coffeewhale",
    author_email="hongkunyoo@gmail.com",
    description="send slack to channel every where",
    license="MIT License",
    keywords="slack api, slack notification",
    url="https://github.com/hongkunyoo/sendslack",
    packages=find_packages(),
    install_requires=['requests'],
    long_description="coffeewhale, a whale that tells you the job is done, when it's done!"
)
