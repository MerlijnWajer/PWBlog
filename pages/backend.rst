Backends
========


A blog entry needs the following:

    -   ID (Name)
    -   Title (maybe?)
    -   Categories (tags)
    -   Creation Date
    -   Data (.html)

Author has the following properties:

    -   ID / Name
    -   Password (hash) *May not be required if the backend is a FS*
    -   Mail

.. code-block:: python

    class PWBlogBackend(object):
        """
        Python WeBlog backend.
        """
        def __init__(self):
            pass

        def lookup_blogpost(self, key):
            """
            Look up a specific post identified by *key*.
            Return a BlogEntry object.
            """

        def get_all_entries():
            """
            Return all entries as a list of BlogEntries
            """

    class BlogEntry(object):
        """
        A Blog post/entry.
        """
        def __init__(self, author, title, categories, creation_date, html_data):
            pass

    class BlogAuthor(object):
        """
        A blog author object.
        """
        def __init__(self, name, mail=None):
            pass

        def get_all_entries(self):
            return []

    class BlogCategory(object):
        def __init__(self, name):
            pass

        def get_all_entries(self):
            return []
