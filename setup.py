import os

from setuptools import find_packages, setup


def read_file(filename):
    with open(os.path.join(os.path.dirname(__file__), filename), encoding="utf-8") as f:
        long_description = f.read()
    return long_description


setup(
    name="bohrium-sdk",
    version="0.13.0",
    author="dingzhaohan",
    author_email="dingzh@dp.tech",
    url="https://github.com/dingzhaohan",
    description="bohrium openapi python sdk",
    long_description=read_file("README.md"),  # detail description for pypi
    long_description_content_type="text/markdown",  # file format
    packages=find_packages("src", exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    package_dir={"": "src"},  # find_packages define code directory
    package_data={
        # include .txt all of them
        "": ["*.txt"]
    },
    install_requires=[
        "distro",
        "httpx",
        "typing_extensions",
        "anyio",
        "pyhumps",
        "requests",
        "tqdm",
    ],
    python_requires=">=3.7",
    entry_points={},
)
