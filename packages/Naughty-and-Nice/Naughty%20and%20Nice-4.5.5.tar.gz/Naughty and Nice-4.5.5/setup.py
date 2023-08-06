from setuptools import setup

__project__ = "Naughty and Nice"
__version__ = "4.5.5"
__description__ = "A program that gets tweets off your API key in tweepy and analyizes a user's acoount on twitter to see if they are naughty or nice."
__packages__ = ["naughty_and_nice"]
__author__ = "Arhith"
__author_email__ = "arhithprem@gmail.com"
__classifiers__ = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Education",
    "Programming Language :: Python :: 3",
]
__keywords__ = ["twitter", "learning"]
__requires__ = ["tweepy", "json", "re", "string", "nltk"]

setup(
    name = __project__,
    version = __version__,
    description = __description__,
    packages = __packages__,
    author = __author__,
    author_email = __author_email__,
    classifiers = __classifiers__,
    keywords = __keywords__,
    requires = __requires__,
)
