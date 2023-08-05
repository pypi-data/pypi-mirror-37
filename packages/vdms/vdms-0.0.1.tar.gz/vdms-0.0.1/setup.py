import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="vdms",
    version="0.0.1",
    author="Luis Remis",
    author_email="luis.remis@intel.com",
    description="VDMS Client Module",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/IntelLabs/vdms",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

