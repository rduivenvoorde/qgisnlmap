
# https://chriswarrick.com/blog/2014/09/15/python-apps-the-right-way-entry_points-and-scripts/

from setuptools import setup

setup(
    name="osmyaml",
    version="0.1.0",
    packages=["osmyaml"],
    entry_points={
        "console_scripts": [
            "osmyaml = osmyaml.__main__:main"
        ]
    },
)
