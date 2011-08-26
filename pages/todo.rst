..
    :Author: Merlijn Wajer
    :Date: 2011-08-25
    :Categories: pwblog, todo
    :Title: TODO for PWBlog

TODO For PWBlog
===============

.. contents:: :depth: 2

*This page would typically not exist in your production blog!*

PWBlog is by no means a product ready for production.


FileSystem Backend [DONE]
-------------------------

Very basic functionality is implemented; it can load and parse *.rst* files
and return the *.html* data.

Attributes
~~~~~~~~~~

All attributes are supported:

    -   Title
    -   Author
    -   Date
    -   Categories

Caching
~~~~~~~

.. DANGER::

    Caching is implemented. There is only one downside: it won't load new files (one
    created after the file is started) to the cache/db until they are
    accessed/loaded at least once.


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
