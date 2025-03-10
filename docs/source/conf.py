# Copyright 2024 Zero ASIC Corporation
# Licensed under the MIT License (see LICENSE for details)

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys

from datetime import date

sys.path.insert(0, os.path.abspath('../..'))

import logik # noqa E402


# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Logik'
copyright = f'2024-{date.today().year}, Zero ASIC'
author = 'Zero ASIC'
release = logik.__version__

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",  # automatically generate documentation for modules
    "sphinx.ext.napoleon",  # to read Google-style or Numpy-style docstrings
    "sphinx.ext.viewcode",  # to allow vieing the source code in the web page
    "autodocsumm"  # to generate tables of functions, attributes, methods, etc.
]

templates_path = ['_templates']
exclude_patterns = []

root_doc = 'index'


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'

autodoc_inherit_docstrings = False
autodoc_typehints = "description"
# include __init__ docstrings
autoclass_content = "both"
