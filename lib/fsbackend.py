# Some of the code in here is terrible. I still need to read up on the best way
# to use utf8 in python


from lib.rst_render import render_rst
import datetime
import os
import stat

import re

def parse_headers(f):
    """
    """
    line = f.readline()
    if not f:
        raise Exception('File invalid')

    if not line.startswith('..'):
        raise Exception('File contains no info')

    contents = ''

    while True:
        line = f.readline()
        if line.startswith('    :') or line.startswith('\t:'):
            contents += line
        else:
            break

    reg = re.compile(':(\w+): (.+)')
    res = reg.findall(contents)

    parsed_obj = dict()
    for name, val in res:
        name = name.lower()
        if name in ('author', 'title'):
            parsed_obj[name] = val.decode('utf8')
        elif name in ('date',):
            try:
                date = datetime.datetime( **dict(zip(['year', 'month', 'day'], \
                        map(lambda x: int(x), val.split('-')))) )
            except TypeError:
                raise Exception('Invalid date: %s' % val)

            parsed_obj[name] = date

        elif name in ('categories',):
            parsed_obj[name] = map(lambda x: x.decode('utf8').strip(), val.split(','))
        else:
            raise Exception('Invalid file data: %s' % name)

    return (f.read(), parsed_obj)

class FSBackend(object):
    """
    Python WeBlog Filesystem backend.
    """
    def __init__(self, path):
        self.path = path

        self.build_db()

    def build_db(self):
        blogs = None

        self._db = {}

        for root, dirs, files in os.walk(self.path):
            if root == self.path:
                blogs = filter(lambda f: f.endswith('.rst'), files)
                break

        if blogs is None:
            return

        for x in blogs:
            e = self.lookup_entry(x[:-4])
            if e is None:
                continue

            st = os.stat(self.path + x)
            self._db[x[:-4]] = dict(obj=e, last_modified=st[stat.ST_MTIME])


    def lookup_entry(self, key):
        """
        Look up a specific post identified by *key*.
        Return a BlogEntry object.
        """
        try:
            st = os.stat(self.path + key + '.rst')
        except OSError, e:
            print 'File does not exist:', e
            return None

        if key in self._db:
            print 'May use cache...'
            if st[stat.ST_MTIME] > self._db[key]['last_modified']:
                print 'File has been modified'
            else:
                print 'File has not been modified. Using cache'
                return self._db[key]['obj']

        try:
            f = open(self.path + key + '.rst')
            data, headers = parse_headers(f)
        except IOError, e:
            print 'Error:', e
            return None

        rst = render_rst(data)

        title = headers['title'] if 'title' in headers else None
        author = headers['author'] if 'author' in headers else None
        date = headers['date'] if 'date' in headers else None
        categories = headers['categories'] if 'categories' in headers else None

        body = rst['html_body']

        entry = FSBlogEntry(key, author, title, categories,
            date, body)

        self._db[key] = dict(obj=entry, last_modified=st[stat.ST_MTIME])

        return entry

    # Maybe an iterator?
    def get_all_entries(self):
        res = []
        for x, y in self._db.iteritems():
            res.append(y['obj'])
        res.sort(key=lambda x: x.creation_date, reverse=True)
        return res

    def get_all_entries_by_category(self, category):
        res = []
        for x, y in self._db.iteritems():
            if category in map(lambda x: x.name, y['obj'].categories):
                res.append(y['obj'])
        res.sort(key=lambda x: x.creation_date, reverse=True)
        return res

    def get_all_authors(self):
        res = {}
        for x, y in self._db.iteritems():
            res[y['obj'].author.name] = None

        return sorted(res.iterkeys(), key=lambda x: x.name)

    def get_all_categories(self):
        res = {}
        for x, y in self._db.iteritems():
            cat = y['obj'].categories
            for x in cat:
                res[x.name] = x

        return sorted(res.itervalues(), key=lambda x: x.name)


class FSBlogEntry(object):
    """
    A Blog post/entry.
    """
    def __init__(self, shortname=None, author=None, title=None, categories=[], \
            creation_date=None, html_data=None):

        self.shortname = shortname
        self.author = FSBlogAuthor(author)
        self.title = title
        self.categories = map(lambda x: FSBlogCategory(x), categories)
        self.creation_date = creation_date
        self.html_data = html_data

class FSBlogAuthor(object):
    """
    A blog author object.
    """
    def __init__(self, name, mail=None):
        self.name = name
        self.mail = mail

class FSBlogCategory(object):
    """
    """
    def __init__(self, name):
        self.name = name
