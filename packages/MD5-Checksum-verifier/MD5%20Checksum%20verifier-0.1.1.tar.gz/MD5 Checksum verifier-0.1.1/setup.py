import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    # Application name:
    name="MD5 Checksum verifier",

    # Version number (initial):
    version="0.1.1",

    # Application author details:
    author="Brendan T D. Jennings",
    author_email="jbrendan70@outlook.com",

    # Packages
    packages=setuptools.find_packages(),

    # Include additional files into the package
    include_package_data=True,

    # Details
    url="https://github.com/dudeisbrendan03/consoleTools",
    long_description=long_description,
    long_description_content_type="text/markdown",

    #
    license="LICENSE",
    description="MD5 Hash (checksum) verification tool",

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
)