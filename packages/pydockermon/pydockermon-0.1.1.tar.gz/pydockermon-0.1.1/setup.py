"""Setup configuration."""
import setuptools

with open("README.md", "r") as fh:
    LONG = fh.read()
setuptools.setup(
    name="pydockermon",
    version="0.1.1",
    author="Joakim Sorensen",
    author_email="ludeeus@gmail.com",
    description="A python module to interact with ha-dockermon.",
    long_description=LONG,
    install_requires=['requests'],
    long_description_content_type="text/markdown",
    url="https://github.com/ludeeus/pydockermon",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
