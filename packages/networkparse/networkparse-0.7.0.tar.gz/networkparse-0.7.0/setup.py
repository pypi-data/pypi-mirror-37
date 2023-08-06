from setuptools import setup, find_packages


with open("README.rst") as f:
    readme = f.read()

with open("LICENSE") as f:
    license = f.read()

version = __import__("networkparse").__version__

setup(
    name="networkparse",
    version=version,
    description="Simple read-only parser for Cisco IOS, NX-OS, and other network device running configs",
    long_description=readme,
    author="Ryan Morehart",
    author_email="ryan@moreharts.com",
    url="https://gitlab.com/xylok/networkparse",
    license=license,
    packages=find_packages(exclude=("tests", "docs")),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
