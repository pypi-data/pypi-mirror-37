import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="vps",
    version="0.0.5",
    author="Andrew Schultz",
    author_email="andrew.schultz@protonmail.com",
    description="Create and Manage VPS Instances",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/aschult5/vps",
    packages=setuptools.find_packages(),
    install_requires=[
        "ovh"
    ],
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

