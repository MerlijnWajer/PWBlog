from sqlalchemy import Table, Column, Integer, String, DateTime, func, \
     ForeignKey, Unicode

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

Base = declarative_base()
metadata = Base.metadata

class SQLBackend(object):
    """
    Python WeBlog SQL backend.
    """
    def __init__(self):
        pass

    def lookup_entry(self, key):
        ret = Session.query(BlogEntry).filter(BlogEntry.shortname == key\
                ).first()
        return ret

    def get_all_entries(self):
        return Session.query(BlogEntry).all()

    def get_all_authors(self):
        return Session.query(BlogAuthor).all()

    def get_all_categories(self):
        return Session.query(BlogCategory).all()

entry_categories = Table('entry_categories', metadata,
        Column('entry_id', Integer, ForeignKey('entries.id')),
        Column('category_id', Integer, ForeignKey('categories.id'))
    )

class BlogEntry(Base):
    """
    A Blog post/entry.
    """
    __tablename__ = 'entries'

    id = Column(Integer, primary_key=True)
    shortname = Column(String(40), unique=True)

    author_id = Column(Integer, ForeignKey('authors.id'))
    author = relationship('BlogAuthor',  backref=backref('entries'),
            order_by=id)

    title = Column(Unicode(100))
    html_data = Column(Unicode)

    creation_date = Column(DateTime, default=func.now())

    def __init__(self, shortname, author, title, categories, \
            creation_date, html_data):

        self.shortname = shortname
        self.author = author
        self.title = title
        self.categories = categories
        self.creation_date = creation_date
        self.html_data = html_data

class BlogAuthor(Base):
    """
    A blog author object.
    """
    __tablename__ = 'authors'

    # entries

    id = Column(Integer, primary_key=True)
    name = Column(Unicode(20), unique=True)
    password = Column(String(64), nullable=False)
    mail = Column(String(40), nullable=True)

    def __init__(self, name, password=None, mail=None):
        self.name = name
        self.password = password
        self.mail = mail

class BlogCategory(Base):
    """
    """
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(Unicode(60), unique=True)

    variables = relationship('BlogEntry', secondary=entry_categories,
        backref='categories')

    def __init__(self, name):
        self.name = name

from lib.sql import *
