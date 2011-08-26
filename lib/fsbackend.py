from lib.rst_render import render_rst
import datetime
import os
import re

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

        rst = render_rst(data)

        title = rst['title'] # FIXME
        body = rst['html_body']

        return FSBlogEntry(_id=key, title=title, html_data=body)

    def get_all_entries(self):
        for root, dirs, files in os.walk(self.path):
            if root == self.path:
                return map(lambda e: FSBlogEntry(_id=e,title=e), map(lambda s: s[:-4],
                    filter(lambda f: f.endswith('.rst'), files)))

        return []

class FSBlogEntry(object):
    """
    A Blog post/entry.
    """
    def __init__(self, _id=None, author=None, title=None, categories=[], \
            creation_date=None, html_data=None):

        self._id, self.author, self.title, self.categories, self.creation_date,\
            self.html_data = _id, author, title, categories, creation_date,\
            html_data

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
