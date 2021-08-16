import os

from setuptools import setup, find_packages


def read(file_name):
    with open(os.path.join(os.path.dirname(__file__), file_name)) as file:
        return file.read()


setup(
    name="fate-of-dice",
    version_config=True,
    setup_requires=['setuptools-git-versioning'],
    author="Kamil Bak",
    author_email="bonczeq.mail@gmail.com",
    description="Discord dice bot",
    long_description=read('README.md'),
    long_description_content_type="text/markdown",
    url="https://github.com/bonczeq/FateOfDice",
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    package_data={'': ['resources/icons/*.png']},
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License"
    ],
    python_requires='>=3.9.6',
    entry_points={
        'console_scripts': ['fate_of_dice = fate_of_dice.main:main'],
    }
)
