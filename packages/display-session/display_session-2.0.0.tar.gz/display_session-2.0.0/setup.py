from setuptools import setup

import display_session
import sys


if sys.version_info[0] >= 3:
    openf = open
else:
    import codecs

    openf = codecs.open


def read(fn):
    with openf(fn, encoding="utf-8") as fp:
        return fp.read()


setup(
    name="display_session",
    version=display_session.__version__,
    description="Convenient formatting, coloring, and utility for user-facing print statements. ",
    long_description=(read("README.rst")),
    url="http://github.com/kdggavkc/display-session/",
    license=display_session.__license__,
    author=display_session.__author__,
    author_email="nickclawrence@gmail.com",
    py_modules=["display_session"],
    install_requires=['colorama>=0.4.0'],
    classifiers=[
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.6",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)