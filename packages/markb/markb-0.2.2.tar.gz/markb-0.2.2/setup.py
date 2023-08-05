import setuptools

from markb import __version__

with open("README.md") as readme:
    long_description = readme.read()

setuptools.setup(
    name="markb",
    version=__version__,
    author="Amir Eldor",
    author_email="amir@eize.ninja",
    description="Render a markdown file and open in a browser",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/amireldor/markb",
    packages=setuptools.find_packages(),
    install_requires=[
        "Markdown"
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Programming Language :: Python :: 3",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
    ],
    scripts=["bin/markb"],
)
