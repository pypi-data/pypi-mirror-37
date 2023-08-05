import setuptools

with open("README.md", "r") as fh:
    _long_description = fh.read()

setuptools.setup(
    name="laylib",
    version="1.1.2",
	license="MIT License",
    description="A 2-D game engine for Python",
    long_description=_long_description,
    author="Amardjia Amine",
    author_email="amardjia.amine@gmail.com",
    url="https://github.com/Layto888/laylib-1.1.2",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
