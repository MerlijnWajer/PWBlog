TODO
====

*This page would typically not exist in your production blog!*

PWBlog is by no means a product ready for production.

Things to do:

    -   Figure out what backend to use, or how to let the user choose from
        one of the following:

            -   SQL backend. (Support for MySQL, PostgreSQL and SQLite)
            -   Filesystem backend. (With optional git support)

    -   Markup language support:

        -   reStructured Text.

    -   Markup languages that may be supported later:

        -   HTML
        -   BBCode

    -   Caching:

        -   Save .rst pages as HTML on startup.
        -   Render the .rst pages everytime to HTML.
        -   Filesystem ``cache``; just have a folder with .html files created of
            .rst files. (Or not created by rst, easy to add html support this way)
