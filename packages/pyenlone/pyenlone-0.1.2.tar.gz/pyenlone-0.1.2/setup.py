import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyenlone",
    version="0.1.2",
    author="QuanticPotato",
    description="A python implementation of enl.one API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/potato-tools/pyenlone",
    packages=setuptools.find_packages(),
    install_requires=[
          'requests',
          'requests_cache',
          'munch',
      ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
