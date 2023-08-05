import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="graviton",
    version="0.0",
    author="Adam Obeng",
    author_email="adamobeng@fb.com",
    description="The Graviton package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/facebookincubator/graviton",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
)
