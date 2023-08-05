"""Setup file for the pip package."""
import setuptools
import os

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dungeon-n-python",
    version="{0}".format(os.environ["VERSION"]),
    include_package_data=True,
    author="Thomas Nicollet, Alexandre Fourcat",
    author_email="thomas.nicollet@epitech.eu, alexandre.fourcat@epitech.eu",
    description="A dungeon which yo must escape",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Afourcat/DungeonAndPython",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
