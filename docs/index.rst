.. _sphinx_json_schema_spec:

.. include:: ../README.rst

Usage
-----

The extension currently provides a single Sphinx `role`:

.. rst:role:: kw

    Link to the current JSON Schema specification's definition of the keyword
    provided.

For instance, writing:

    .. code-block:: rst

        Reference resolution in JSON Schema is done using the :kw:`$ref` keyword.

will produce:

    Reference resolution in JSON Schema is done using the :kw:`$ref` keyword.

What's here, albeit crude, has been used in some form for a long while by `jsonschema` (the Python library), but the hope is it may be useful to alternate implementations or users in general.
Help is very much welcome to improve it!

In the future support may be added for linking to different drafts, or for linking to `Understanding JSON Schema <https://json-schema.org/understanding-json-schema/index.html>`_.
