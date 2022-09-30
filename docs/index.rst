.. _sphinx_json_schema_spec:

.. include:: ../README.rst

Usage
-----

The extension currently provides a single Sphinx `role`:

.. rst:role:: kw

    Link to the current JSON Schema specification's definition of the keyword provided.

For instance, writing:

    .. code-block:: rst

        Reference resolution in JSON Schema is done using the :kw:`$ref` keyword.

will produce:

    Reference resolution in JSON Schema is done using the :kw:`$ref` keyword.

In addition, the extension automatically populates the Sphinx glossary with terms from the `JSON Schema Glossary <https://json-schema.org/learn/glossary.html>`_, such that:

    .. code-block:: rst

        If a :term:`schema` has a :term:`meta-schema`, what do :term:`meta-schemas <meta-schema>` have?

will produce:

    If a :term:`schema` has a :term:`meta-schema`, what do :term:`meta-schemas <meta-schema>` have?


Contributing
------------

What's here, albeit crude, has been used in some form for a long while by `jsonschema` (the Python library), but the hope is it may be useful to alternate implementations or users in general.
Help is very much welcome to improve it!

In particular, help adding support for other (historic or future) drafts, rather than just the single draft currently supported, would be great.
