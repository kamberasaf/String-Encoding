"""
Setup script for the string-encoding package.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="string-encoding",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A custom Python string class with advanced encoding and transformation features",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kamberasaf/string-encoding",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing",
    ],
    python_requires=">=3.6",
)