import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nesterlists",
    version="1.0.0",
    license="MIT License",
    author="Marciodm",
    author_email="marcio0770@gmail.com",
    description="Returns items in lists that may or may not include nested lists.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Marciodm",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
    ),
)
