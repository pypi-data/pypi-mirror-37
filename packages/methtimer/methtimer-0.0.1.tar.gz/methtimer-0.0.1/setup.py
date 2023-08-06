import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="methtimer",
    version="0.0.1",
    author="AbiramK",
    author_email="abiramkannan99@outlook.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/AbiramK/methtimer",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
    ],
)