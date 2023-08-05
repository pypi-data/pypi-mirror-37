import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="avmu",
    version="0.0.1",
    author="Connor Wolf, Akela Inc",
    author_email="cwolf@akelainc.com",
    description="Control interface and API for running Akela Vector Measurement Units.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AkelaInc/avmu",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
    ],
)