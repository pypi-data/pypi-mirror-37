import sys
import setuptools

if sys.version_info[0:2] < (3, 5):
    raise Exception("pybinder requires Python 3.5+")

setuptools.setup(
    name="pybinder",
    version="0.0.1",
    author="heyike",
    author_email="heyike1993@gmail.com",
    description="",
    url="https://github.com/heyike/pybinder",
    packages=["pybinder"],
)