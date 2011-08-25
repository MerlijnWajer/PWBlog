from lib.rst_render import render_rst
import datetime
import os

class FSPWBlogBackend(object):
    """
    Python WeBlog backend.
    """
    def __init__(self, path):
        self.path = path

    def lookup_entry(self, key):
        """
        Look up a specific post identified by *key*.
        Return a BlogEntry object.
        """

        try:
            f = open(self.path + key + '.rst')
            data = f.read()
        except IOError, e:
            print 'Error:', e
            return None

        rst = render_rst(data)['html_body']

        b = FSBlogEntry(author=None, title=key, categories=[],
                creation_date=datetime.datetime.now(), html_data=rst)

        return b

    def get_all_entries(self):
        return []

class FSBlogEntry(object):
    """
    A Blog post/entry.
    """
    def __init__(self, author, title, categories, creation_date, html_data):
        self.author, self.title, self.categories, self.creation_date, \
            self.html_data = \
            author, title, categories, creation_date, html_data
        pass

class FSBlogAuthor(object):
    """
    A blog author object.
    """
    def __init__(self, name, mail=None):
        pass

    def get_all_entries(self):
        return []

class FSBlogCategory(object):
    """
    """
    def __init__(self, name):
        pass

    def get_all_entries(self):
        return []
