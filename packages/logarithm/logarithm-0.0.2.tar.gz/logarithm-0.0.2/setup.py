import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="logarithm",
    version="0.0.2",
    author="Alex Romantsov",
    author_email="dadakil486@gmai.com",
    description="Function to find the logarithm",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AlexRomantsov/logarithm",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)