import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="libinfilect",
    version="0.0.1",
    author="Tushar Pawar",
    author_email="tushar@infilect.com",
    description="Collection of frequently used utility functions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://bitbucket.org/infilect-ml-dev/libinfilect/",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ),
)