import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="vatstat",
    version="0.0.3",
    author="Ryan Null",
    author_email="ryan.null@gmail.com",
    description="python api that makes interacting with the VATSIM data less painful and more pragmatic.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/BIGjuevos/vatstat",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
