import os
import setuptools


def read(file_name):
    return open(os.path.join(os.path.dirname(__file__), file_name)).read()


setuptools.setup(
    name="FateOfDice",
    version="0.0.1",
    author="Kamil Bak",
    author_email="bonczeq.mail@gmail.com",
    description="Discord dice bot",
    long_description=read('README.md'),
    long_description_content_type="text/markdown",
    url="https://github.com/bonczeq/FateOfDice",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3"
    ],
    python_requires='>=3.9',
)
