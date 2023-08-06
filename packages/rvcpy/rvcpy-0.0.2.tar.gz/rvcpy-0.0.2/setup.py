import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rvcpy",
    version="0.0.2",
    author="Ruben Van Coile",
    author_email="ruben.vancoile@gmail.com",
    description="rvc basic functionality",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rvcoile/rvcpy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)