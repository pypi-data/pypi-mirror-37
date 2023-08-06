import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="giossync",
    version="0.0.1",
    author="Marcin Grom",
    author_email="marcin.grom@gmail.com",
    description="asyncio-friendly python API for gios",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mgrom/giossync",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.4",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)