# -*- coding: utf-8 -*-
# pylint: disable=all
"""Tolkein documentation config."""

import os
import sys
import traceback

sys.path.insert(0, os.path.abspath("../src"))

print(sys.path)

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.coverage",
    "sphinx.ext.doctest",
    "sphinx.ext.extlinks",
    "sphinx.ext.ifconfig",
    "sphinx.ext.napoleon",
    "sphinx.ext.todo",
    "sphinx.ext.viewcode",
]
source_suffix = ".rst"
master_doc = "index"
project = "Tolkein"
year = "2020"
author = "Tolkit"
author_email = "tolkein@genomehubs.org"
copyright = "{0}, {1}".format(year, author)
try:
    from pkg_resources import get_distribution

    version = release = get_distribution("tolkein").version
except Exception:
    traceback.print_exc()
    version = release = "0.5.0"

pygments_style = "trac"
templates_path = ["."]
extlinks = {
    "issue": ("https://github.com/tolkit/tolkein/issues/%s", "#"),
    "pr": ("https://github.com/tolkit/tolkein/pull/%s", "PR #"),
}
# on_rtd is whether we are on readthedocs.org
on_rtd = os.environ.get("READTHEDOCS", None) == "True"

if not on_rtd:  # only set the theme if we're building docs locally
    html_theme = "sphinx_rtd_theme"

html_use_smartypants = True
html_last_updated_fmt = "%b %d, %Y"
html_split_index = False
html_sidebars = {
    "**": ["searchbox.html", "globaltoc.html", "sourcelink.html"],
}
html_short_title = "%s-%s" % (project, version)

# napoleon_use_ivar = True
# napoleon_use_rtype = False
# napoleon_use_param = False
# Napoleon settings
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_type_aliases = None
