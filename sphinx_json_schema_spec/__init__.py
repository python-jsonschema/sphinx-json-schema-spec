from contextlib import suppress
from datetime import datetime
from pathlib import Path
from urllib.parse import urljoin
import ssl
import urllib.request

try:
    from importlib import metadata
except ImportError:
    import importlib_metadata as metadata  # type: ignore

from docutils import nodes
from lxml import html

BASE_URL = "https://json-schema.org/draft/2020-12/"
VOCABULARIES = {
    "core": urljoin(BASE_URL, "json-schema-core.html"),
    "validation": urljoin(BASE_URL, "json-schema-validation.html"),
}
HARDCODED = {
    "$dynamicRef": "https://json-schema.org/draft/2020-12/json-schema-core.html#dynamic-ref",                        # noqa: E501
    "$ref": "https://json-schema.org/draft/2020-12/json-schema-core.html#ref",
    "format": "https://json-schema.org/draft/2020-12/json-schema-validation.html#name-implementation-requirements",  # noqa: E501
}


def setup(app):
    """
    Install the plugin.

    Arguments:

        app (sphinx.application.Sphinx):

            the Sphinx application context
    """

    app.add_config_value("cache_path", "_cache", "")

    CACHE = Path(app.config.cache_path)
    CACHE.mkdir(exist_ok=True)

    documents = {
        url: fetch_or_load(cache_path=CACHE / f"{name}.html", url=url)
        for name, url in VOCABULARIES.items()
    }
    app.add_role("kw", docutils_does_not_allow_using_classes(documents))

    glossary = fetch_or_load(
        cache_path=CACHE / "glossary.html",
        url="https://json-schema.org/learn/glossary.html",
    )
    app.connect("missing-reference", missing_reference(glossary))

    return dict(parallel_read_safe=True)


def fetch_or_load(cache_path, url):
    """
    Fetch a new page or specification, or use the cache if it's current.

    Arguments:

        cache_path:

            the local path to a (possibly not yet existing) cache for the file

        url:

            the URL of the document
    """

    version = metadata.version("sphinx-json-schema-spec")
    headers = {"User-Agent": f"sphinx-json-schema-spec v{version}"}

    with suppress(FileNotFoundError):
        modified = datetime.utcfromtimestamp(cache_path.stat().st_mtime)
        date = modified.strftime("%a, %d %b %Y %I:%M:%S UTC")
        headers["If-Modified-Since"] = date

    request = urllib.request.Request(url, headers=headers)
    context = ssl.create_default_context()
    response = urllib.request.urlopen(request, context=context)

    if response.code == 200:
        with cache_path.open("w+b") as out:
            out.writelines(response)
            out.seek(0)
            return html.parse(out).getroot()

    return html.parse(cache_path.read_bytes()).getroot()


def docutils_does_not_allow_using_classes(vocabularies):
    """
    Yeah.

    It doesn't allow using a class because it does annoying stuff like
    try to set attributes on the callable object rather than just
    keeping a dict.
    """

    def keyword(name, raw_text, text, lineno, inliner):
        """
        Link to the JSON Schema documentation for a keyword.

        Arguments:

            name (str):

                the name of the role in the document

            raw_source (str):

                the raw text (role with argument)

            text (str):

                the argument given to the role

            lineno (int):

                the line number

            inliner (docutils.parsers.rst.states.Inliner):

                the inliner

        Returns:

            tuple:

                a 2-tuple of nodes to insert into the document and an
                iterable of system messages, both possibly empty
        """

        hardcoded = HARDCODED.get(text)
        if hardcoded is not None:
            return [nodes.reference(raw_text, text, refuri=hardcoded)], []

        # find the header in the validation spec containing matching text
        for vocabulary_url, spec in vocabularies.items():
            lower = text.lstrip("$").lower()
            header = spec.get_element_by_id(f"name-{lower}", None)
            if header is None:
                header = spec.get_element_by_id(
                    f"name-the-{lower}-keyword",
                    None,
                )

            if header is not None:
                uri = urljoin(vocabulary_url, header.find("a").attrib["href"])
                break
        else:
            inliner.reporter.warning(
                "Didn't find a target for {0}".format(text),
            )
            uri = BASE_URL

        reference = nodes.reference(raw_text, text, refuri=uri)
        return [reference], []

    return keyword


def missing_reference(glossary):

    terms = {
        link.lstrip("#")
        for _, _, link, _ in glossary.iterlinks()
        if link.startswith("#")
    }

    def _missing_reference(app, env, node, contnod):
        """
        Resolve a reference to a JSON Schema Glossary term.
        """

        if node["reftype"] != "term":
            return

        target = node["reftarget"]
        if target not in terms:
            return

        uri = f"https://json-schema.org/learn/glossary.html#{target}"

        text = contnod.astext() if node["refexplicit"] else target
        return nodes.reference(text, text, internal=False, refuri=uri)
    return _missing_reference
