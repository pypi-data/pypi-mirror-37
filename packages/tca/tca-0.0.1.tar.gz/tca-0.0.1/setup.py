import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tca",
    version="0.0.1",
    author="Ana Ruelas",
    author_email="anaruelas@gmail.com",
    description="A TCA package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ahgnaw/tca",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
