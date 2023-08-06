import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tag_fixer",
    version="0.0.1",
    author="Kristopher Kyle",
    author_email="kristopherkyle1@gmail.com",
    description="A simple interface for checking and fixing POS tags",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kristopherkyle/tag_fixer",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)