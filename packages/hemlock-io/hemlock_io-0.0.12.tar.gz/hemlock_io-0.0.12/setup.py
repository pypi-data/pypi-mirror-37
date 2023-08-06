import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hemlock_io",
    version="0.0.12",
    author="John Alexander Harris",
    author_email="john@hemlock.io",
    description="Helper package for transferring data to server",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hemlock-io/hemlock_io",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
