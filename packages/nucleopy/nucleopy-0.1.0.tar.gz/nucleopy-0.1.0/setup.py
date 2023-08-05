import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nucleopy",
    version="0.1.0",
    author="Rohan Koodli",
    author_email="rovik05@gmail.com",
    description="A library for creating and manipulating RNA and DNA sequences",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/RK900/nucleopy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
	"Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
