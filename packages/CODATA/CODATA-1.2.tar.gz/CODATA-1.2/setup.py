import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="CODATA",
    version="1.2",
    author="Jelle Westra",
    author_email="jelwestra@gmail.com",
    description="""All CODATA constants with units, uncertainty and
                description.""",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JelleWestra/CODATA",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
