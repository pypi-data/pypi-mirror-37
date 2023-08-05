import setuptools

name = "rautils"
version = "1.0.10"
author = "Parth S. Patel"
author_email = "parthspatel.nj@gmail.com"
description = "Python utility for file manipulation"
long_description_content_type = "text/markdown"
url = "https://github.com/parthspatel/rautils"

classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
]

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name=name,
    version=version,
    author=author,
    author_email=author_email,
    description=description,
    long_description=long_description,
    long_description_content_type=long_description_content_type,
    url=url,
    packages=setuptools.find_packages(),
    classifiers=classifiers,
)
