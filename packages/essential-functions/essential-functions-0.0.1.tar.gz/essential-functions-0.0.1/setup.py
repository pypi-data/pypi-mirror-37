import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="essential-functions",
    version="0.0.1",
    author="Nabarun Pal",
    author_email="pal.nabarun95@gmail.com",
    description="Simple package to try out packaging",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/palnabarun/essential-functions",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)