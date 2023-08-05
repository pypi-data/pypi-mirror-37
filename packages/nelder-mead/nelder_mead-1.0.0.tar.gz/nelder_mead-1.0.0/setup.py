# from distutils.core import setup
from setuptools import setup
from nelder_mead import __version__

# prevent the error when building Windows .exe
import codecs
try:
    codecs.lookup('mbcs')
except LookupError:
    ascii = codecs.lookup('ascii')
    func = lambda name, enc=ascii: {True: enc}.get(name=='mbcs')
    codecs.register(func)

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name="nelder_mead",
      long_description=long_description,
      version=__version__, # __version__.split()[0]
      description="Nelder-Mead " +
                  "for numerical optimization in Python",
      author="Masahiro Nomura",
      author_email="masahironomura5325@gmail.com",
      maintainer="Masahiro Nomura",
      maintainer_email="masahironomura5325@gmail.com",
      url="https://github.com/nmasahiro/nelder_mead",
      license="MIT",
      classifiers = [
          "Intended Audience :: Science/Research",
          "Intended Audience :: Education",
          "Intended Audience :: Other Audience",
          "Topic :: Scientific/Engineering",
          "Topic :: Scientific/Engineering :: Mathematics",
          "Topic :: Scientific/Engineering :: Artificial Intelligence",
          "Operating System :: OS Independent",
          "Programming Language :: Python :: 3",
          "Development Status :: 4 - Beta",
          "Environment :: Console",
          "License :: OSI Approved :: MIT License",
      ],
      keywords=["optimization", "Nelder-Mead"],
      packages=["nelder_mead"],
      requires=["numpy", "functools"],
      package_data={'': ['LICENSE']},  # i.e. cma/LICENSE
      )