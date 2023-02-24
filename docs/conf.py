import sys
from pathlib import Path

sys.path.insert(0, str(Path("../..").resolve()))

project = "blender_addon_utils"
author = "30350n"

version = "0.1"
release = "0.1"

extensions = [
    "sphinx.ext.duration",
    "sphinx.ext.doctest",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.intersphinx",
]

intersphinx_mapping = {"python": ("https://docs.python.org/3", None)}
html_theme = "sphinx_rtd_theme"
epub_show_urls = "footnote"
add_module_names = False
