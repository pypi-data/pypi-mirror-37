import setuptools
from opensignalsreader import __author__, __version__, __email__, name, description

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name=name,
    version=__version__,
    author=__author__,
    author_email=__email__,
    description=description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/PGomes92/opensignalsreader",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)