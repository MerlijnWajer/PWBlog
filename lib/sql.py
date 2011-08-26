import sqlalchemy
from sqlalchemy import create_engine

#try:
#    from credentials import dbu, dbpwd, dwh, dbp, dbname
#except ImportError, e:
#    print 'Cannot find credentials!'

#engine = create_engine("postgresql+psycopg2://%s:%s@%s:%s/%s" % (dbu, dbpwd,
#    dwh, dbp, dbname))
engine = create_engine('sqlite:///blog.db', echo=True)

# Pass echo=True to see all SQL queries
# When using MySQL; pass charset=utf8&use_unicode=1

from lib.sqlbackend import Base, BlogEntry, BlogAuthor, BlogCategory

Base.metadata.create_all(engine)
metadata = Base.metadata
from sqlalchemy.orm import scoped_session, sessionmaker
Session = scoped_session(sessionmaker(bind=engine))
