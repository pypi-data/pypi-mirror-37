import sqlite3
import os
from fbetl.extractors.comments  import Comments
from fbetl.extractors.messages  import Messages
from fbetl.extractors.posts     import Posts
from fbetl.extractors.reactions import Reactions

class FbetlError(Exception):
    pass


class Fbetl(object):
  def __init__(self, path):
    if not isinstance(path, str):
      raise FbetlError('path should be string')

    self.db   = sqlite3.connect(':memory:')
    self.path = os.path.abspath(path)

  def load_comments(self):
    Comments(self.db, self.path)

  def load_messages(self):
    Messages(self.db, self.path)

  def load_posts(self):
    Posts(self.db, self.path)

  def load_reactions(self):
    Reactions(self.db, self.path)

  def load_all(self):
    self.load_comments()
    self.load_messages()
    self.load_posts()
    self.load_reactions()

  def sql(self, query):
    return self.db.execute(query).fetchall()

  def save(self, path):
    disk_db = sqlite3.connect(path)
    with disk_db:
      for line in self.db.iterdump():
        if line not in ('BEGIN;', 'COMMIT;'): # let python handle the transactions
          disk_db.execute(line)
    disk_db.commit()
