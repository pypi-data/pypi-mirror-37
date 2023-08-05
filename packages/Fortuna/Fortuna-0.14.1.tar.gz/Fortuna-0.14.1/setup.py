from setuptools import setup, Extension
from Cython.Build import cythonize

""" 
    python3 setup.py sdist bdist_wheel
    twine upload dist/*
    pip install Fortuna
"""


with open("README.md", "r") as fh:
    long_description = fh.read()


setup(ext_modules=cythonize(
    Extension(
        name="Fortuna",
        sources=["Fortuna.pyx"],
        language=["c++"],
        extra_compile_args=["-std=c++17"]
    )),
    name="Fortuna",
    author="Robert Sharp",
    author_email="webmaster@sharpdesigndigital.com",
    url="https://sharpdesigndigital.com",
    requires=["Cython"],
    version="0.14.1",
    description="Fast & Flexible Random Value Generator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=["fortuna_extras"],
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords=[
        "Fortuna", "Random Patterns", "Data Perturbation", "Game Dice", "Weighted Choice", "Random Cycle",
        "Random Value", "Gaussian Distribution", "Linear Geometric Distribution", "The Truffle Shuffle"
    ],
)
