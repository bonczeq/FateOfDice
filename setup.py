import os
from setuptools import setup


def read(file_name):
    return open(os.path.join(os.path.dirname(__file__), file_name)).read()


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
    package_dir={'': 'src'},
    packages=['fate_of_dice'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)",
    ],
    python_requires='>=3.8',
    entry_points={
        'console_scripts': ['fate_of_dice = fate_of_dice.__main__'],
    }
)
