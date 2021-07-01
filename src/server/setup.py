from pathlib import Path

from setuptools import setup

NAME = "palms-server"
VERSION = "0.1.0"
DESCRIPTION = "Precision Accurate LIBS Movement System"
KEYWORDS = "LIBS spectroscopy laser robotics positioning movement"
URL = "https://github.com/RE-PALMS/PALMS"
AUTHOR = "PALMS"
AUTHOR_EMAIL = "22gshaked@ransomeverglades.org"
LICENSE = "MIT"

HERE = Path(__file__).parents[2]
README = (HERE / "README.md").read_text()

CLASSIFIERS = [
    "Environment :: No Input/Output (Daemon)",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3 :: Only",
    "Natural Language :: English",
]

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=README,
    long_description_content_type="text/markdown",
    url=URL,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license=LICENSE,
    classifiers=CLASSIFIERS,
    keywords=KEYWORDS,
    packages=["server"],
    include_package_data=True,
    install_requires=["RPi.GPIO==0.7.0"],
    python_requires=">=3.6",
)
