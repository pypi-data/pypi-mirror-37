from setuptools import setup, Extension
from Cython.Build import cythonize


setup(ext_modules=cythonize(
    Extension(
        name="Fortuna",
        sources=["Fortuna.pyx"],
        language=["c++"],
        extra_compile_args=["-std=c++17"]
    )),
    name="Fortuna",
    author="Robert Sharp",
    requires=["Cython"],
    version="0.15.1",
    description="Fast & Flexible Random Value Generator",
    packages=["fortuna_extras"]
)
