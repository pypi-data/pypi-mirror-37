#!/usr/bin/env python3

import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

from distutils.core import setup
setup(name="wiktfinnish",
      version="0.1.1",
      description="Finnish morphology (including verb forms, comparatives, cases, possessives, clitics)",
      long_description=long_description,
      long_description_content_type="text/markdown",
      author="Tatu Ylonen",
      author_email="ylo@clausal.com",
      url="https://clausal.com",
      license="MIT",
      download_url="https://github.com/tatuylonen/wiktfinnish",
      packages=["wiktfinnish"],
      # install_requires=[],
      classifiers=[
          "Development Status :: 3 - Alpha",
          "Intended Audience :: Developers",
          "Intended Audience :: Science/Research",
          "License :: OSI Approved :: MIT License",
          "Natural Language :: Finnish",
          "Operating System :: OS Independent",
          "Operating System :: POSIX :: Linux",
          "Programming Language :: Python",
          "Programming Language :: Python :: 3.6",
          "Programming Language :: Python :: 3.7",
          "Programming Language :: Python :: 3 :: Only",
          "Topic :: Text Processing",
          "Topic :: Text Processing :: Linguistic",
          ])
