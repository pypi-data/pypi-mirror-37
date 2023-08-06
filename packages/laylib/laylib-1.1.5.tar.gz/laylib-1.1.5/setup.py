import setuptools

_version_ = "1.1.5"
_url_ = "https://github.com/Layto888/laylib"

with open("README.rst", "r") as fh:
    _long_description = fh.read()

setuptools.setup(
    name="laylib",
    version=_version_,
    license="MIT License",
    description="A 2-D engine for Python and pygame",
    long_description=_long_description,
    author="Amardjia Amine",
    author_email="amardjia.amine@gmail.com",
    url=_url_,
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)

