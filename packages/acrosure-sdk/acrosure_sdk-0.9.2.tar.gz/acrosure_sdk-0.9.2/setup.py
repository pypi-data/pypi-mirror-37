import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="acrosure_sdk",
    version="0.9.2",
    author="Jetarin Chokchaipermpoonphol",
    author_email="jetarin.min@gmail.com",
    description="SDK for Acrosure api",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jetarin-min/acrosure-py-sdk",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
