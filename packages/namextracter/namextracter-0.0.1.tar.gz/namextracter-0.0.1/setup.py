import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="namextracter",
    version="0.0.1",
    author="sam-iau",
    author_email="sam-iau@outlook.com",
    description="A lite library for extracting names from text using nltk wordnet",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/frier-sam/namextracter",
    packages=setuptools.find_packages(),
    install_requires=[
          'nltk==3.3'
      ],
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)