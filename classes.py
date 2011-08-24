from sqlalchemy import Table, Column, Integer, String, DateTime, func, \
     ForeignKey, Unicode, Text

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

Base = declarative_base()
metadata = Base.metadata

class User(Base):

    """

    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(Unicode(20), unique=True)
    password = Column(String(64), nullable=False)
    mail = Column(String(40), nullable=True)

    def __init__(self, name, password, mail=None):
        self.name = name
        self.password = password
        self.mail = mail

    def __repr__(self):
        return 'User(%s)' % self.name.encode('utf8')

class Entry(Base):
    __tablename__ = 'entries'

    id = Column(Integer, primary_key=True)
    owner_id = Column(Text(convert_unicode=True), ForeignKey('users.id'))

    title = Column(Unicode(100))
    data = Column(Unicode)

