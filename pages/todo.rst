TODO For PWBlog
===============

.. contents:: :depth: 2

*This page would typically not exist in your production blog!*

PWBlog is by no means a product ready for production.


FileSystem Backend
------------------

Very basic functionality is implemented; it can load and parse *.rst* files
and return the *.html* data.

Attributes
~~~~~~~~~~

It now needs to support more attributes:

    -   Title. ``rst_parts['title']``
    -   Author. (Use one folder per author?)
    -   Creation Date (Use stat(), or parse)
    -   Categories (Parse)

Caching
~~~~~~~

It's a good idea to cache the *.rst* -> *.html* conversions; and only parse the
*.rst* files again if their modification date has changed.

We'll also need to build some sort of mini database to implement operations such
as *get_all_entries()*. The database should incorporate caching.

SQL Backend
-----------

TODO

Custom RST Directives
---------------------

Might be interesting?

Source RST Download
-------------------

Allowing downloading the original *rst*, if available.

PDF Download
------------

If possible, allow pdf conversion and download.

Table of contents
-----------------

Perhaps specification? And it would be nice to have it on the right.


Markup Languages
----------------

Supported:

    -   reStructured Text.

Unsupported:

    -   HTML
    -   BBCode
