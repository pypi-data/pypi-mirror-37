from codecs import open
from distutils.core import setup
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="pyconio",
    version="0.01",
    description="Cross-Platform Python Console I/O.",
    long_description=long_description,
    url="https://pypi.org/pypi/pyconio",
    author="konniskatt",
    license="GNU GPL v2",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Utilities',
        'Topic :: Terminals',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Programming Language :: Python :: 3',
        'Environment :: Console :: Win32 (MS Windows)'
        'Environment :: Console',
    ],
    keywords="pyconio colorama colors termcolor conio console cross-platform gotoxy",
    packages=["pyconio"],
    package_dir={"pyconio": "pyconio"}
)
