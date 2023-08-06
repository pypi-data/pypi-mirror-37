from setuptools import setup

__project__ = "grass_script"
__version__ = "0.0.3"
__description__ = "A Python module that is basically a programming language"
__packages__ = ["grass_script"]
__author__ = "TheOnlyWalrus"
__classifiers__ = [
    "Development Status :: 3 - Alpha",
    "Programming Language :: Python :: 3",
]

setup(
    name = __project__,
    version = __version__,
    description = __description__,
    packages = __packages__,
    author = __author__,
    classifiers = __classifiers__,
)