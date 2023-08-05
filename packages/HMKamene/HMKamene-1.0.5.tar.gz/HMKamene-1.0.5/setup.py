from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="HMKamene",
    version="1.0.5",
    author="HM",
    description="A package contains a generic functions and classes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=find_packages(),
    python_requires='>=3',
    install_requires=[
          'HMGeneric',
          'kamene',
      ],
    classifiers=[
        "Programming Language :: Python :: 3",
        'License :: OSI Approved :: MIT License',
        "Operating System :: OS Independent",
    ],
)