import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ajsonapi",
    version="0.0.0",
    author="Roel van der Goot",
    author_email="roelvandergoot@gmail.com",
    description="An asynchronous JSON API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/rvdg/ajsonapi",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
