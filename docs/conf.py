import importlib.metadata
import re

project = "sphinx-json-schema-spec"
author = "Julian Berman"
copyright = "2013, " + author

release = importlib.metadata.version("sphinx_json_schema_spec")
version = release.partition("-")[0]

language = "en"
default_role = "any"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosectionlabel",
    "sphinx.ext.coverage",
    "sphinx.ext.doctest",
    "sphinx.ext.intersphinx",
    "sphinx.ext.napoleon",
    "sphinx.ext.todo",
    "sphinx_json_schema_spec",
    "sphinxcontrib.spelling",
    "sphinxext.opengraph",
]

pygments_style = "lovelace"
pygments_dark_style = "one-dark"

html_theme = "furo"


def entire_domain(host):
    return r"http.?://" + re.escape(host) + r"($|/.*)"


linkcheck_ignore = [
    entire_domain("img.shields.io"),
    "https://github.com/python-jsonschema/sphinx-json-schema-spec/actions",
    "https://github.com/python-jsonschema/sphinx-json-schema-spec/workflows/CI/badge.svg",  # noqa: E501
]

# = Extensions =

# -- autosectionlabel --

autosectionlabel_prefix_document = True

# -- intersphinx --

intersphinx_mapping = {
    "jsonschema": (
        "https://python-jsonschema.readthedocs.io/en/latest/", None,
    ),
    "packaging": ("https://packaging.python.org/", None),
    "python": ("https://docs.python.org/", None),
    "sphinx": ("https://www.sphinx-doc.org/en/master/", None),
}

# -- sphinxcontrib-spelling --

spelling_word_list_filename = "spelling-wordlist.txt"
spelling_show_suggestions = True
