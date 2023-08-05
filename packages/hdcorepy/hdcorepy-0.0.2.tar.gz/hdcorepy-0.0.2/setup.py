import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hdcorepy",
    version="0.0.2",
    author="John Paul K J",
    author_email="polestar2john@gmail.com",
    description="A simple framework for using the HostDime API in Python",
    url="https://github.com/jpadmin/Hdcore",
    long_description=long_description ,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ]
)
