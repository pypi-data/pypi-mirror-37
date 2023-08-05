import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cpgen",
    version="0.0.2",
    author="Vipul Kumar",
    author_email="finn98@protonmail.com",
    description="Random test-cases generator for competitive programming",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/finn02/generator",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)