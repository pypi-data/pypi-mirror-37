import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="swisshydrodata",
    version="0.0.3",
    author="Bouni",
    author_email="bouni@owee.de",
    description="A library to fetch data from the Swiss federal Office for Environment FEON",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bouni/swisshydrodata",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
