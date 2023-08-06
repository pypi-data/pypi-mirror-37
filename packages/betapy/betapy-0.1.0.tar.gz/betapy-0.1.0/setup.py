import numpy
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
    
setuptools.setup(
    name="betapy",
    version="0.1.0",
    author="Derek Fujimoto",
    author_email="fujimoto@phas.ubc.ca",
    description="bdata interface object",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://ms-code.phas.ubc.ca:2633/dfujim_public/betapy",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ),
    install_requires=['bdata>=1.2'],
)


