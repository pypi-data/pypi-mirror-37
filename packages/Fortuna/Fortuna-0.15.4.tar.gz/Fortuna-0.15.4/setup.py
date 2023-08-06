from setuptools import setup, Extension
from Cython.Build import cythonize

""" 
Local:
    python3 setup.py build_ext --inplace --force

PIP:
    python3 setup.py sdist bdist_wheel
    twine upload dist/*
    pip install Fortuna
"""


with open("README.md", "r") as file:
    long_description = file.read()

setup(ext_modules=cythonize(
        Extension(
            name="Fortuna",
            sources=["Fortuna.pyx"],
            language=["c++"],
            extra_compile_args=["-std=c++17"],
        ),
        compiler_directives={
            'embedsignature': True,
            'language_level': 3,
        },
    ),
    name="Fortuna",
    author="Robert Sharp",
    author_email="webmaster@sharpdesigndigital.com",
    url="https://sharpdesigndigital.com",
    requires=["Cython"],
    version="0.15.4",
    description="Fast & Flexible Random Value Generator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=["fortuna_extras"],
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        'Development Status :: 4 - Beta',
    ],
    keywords=[
        "Fortuna", "Random Patterns", "Data Perturbation", "Game Dice", "Weighted Choice", "Random Cycle",
        "Random Value", "Gaussian Distribution", "Linear Geometric Distribution", "The Truffle Shuffle"
    ],
    python_requires='>=3.6',
)
