from codecs import open
from distutils.core import setup
from os import path

here = path.abspath(path.dirname(__file__))
"""
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()
"""
setup(
    name="pyconio",
    version="0.020",
    description="Cross-Platform Python Console I/O.",
    long_description="Click on homepage for docs.",
    url="https://gitlab.com/konniskatt/pyconio",
    author="konniskatt",
    license="GNU GPL v2",
    keywords="pyconio colorama colors termcolor conio console cross-platform gotoxy",
    packages=["pyconio"],
    package_dir={"pyconio": "pyconio"}
)
