import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Whitelisting",
    version="1.0",
    author="George Westwater",
    author_email="gmwestwater@hotmail.co.uk",
    description="A whitelist automation tool for the MTD API team",
    long_description=long_description,
    url="https://github.com/westwater/mtd-whitelisting",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    )
)
