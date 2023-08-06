from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="pypassgen",
    version="0.1.0",
    author="Ashley Marando",
    author_email="a.marando@me.com",
    description="A python random password generator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    # url="",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
)
