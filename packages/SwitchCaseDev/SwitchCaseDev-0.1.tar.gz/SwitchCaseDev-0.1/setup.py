from setuptools import setup

long_description=''

with open('README.rst') as f:
    long_description=f.read()

setup(
    name="SwitchCaseDev",
    version='0.1',
    author="Ayan Bag",
    description="Python implementation of Switch-Case",
    long_description=long_description,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    
)