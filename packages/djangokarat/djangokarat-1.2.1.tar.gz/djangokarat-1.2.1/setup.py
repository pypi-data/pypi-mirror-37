import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="djangokarat",
    version="1.2.1",
    author="David Simonyi",
    author_email="david@whys.eu",
    description="ability to create models with send/accept fields to/from karat DB",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    url="https://kiwi.whys.eu/karaterp/axima-agent",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
