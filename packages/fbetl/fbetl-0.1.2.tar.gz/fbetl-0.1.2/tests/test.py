import unittest
from fbetl import Fbetl

class TestFbetl(unittest.TestCase):

  def test_load_comments(self):
    fbetl = Fbetl('tests/facebook-user')
    fbetl.load_comments()

    comments_count = fbetl.sql('SELECT COUNT(*) FROM comments;')[0][0]
    self.assertTrue(comments_count == 4)

  def test_load_reactions(self):
    fbetl = Fbetl('tests/facebook-user')
    fbetl.load_reactions()

    reactions_count = fbetl.sql('SELECT COUNT(*) FROM reactions;')[0][0]
    self.assertTrue(reactions_count == 2)

  def test_load_messages(self):
    fbetl = Fbetl('tests/facebook-user')
    fbetl.load_messages()

    messages_count = fbetl.sql('SELECT COUNT(*) FROM messages;')[0][0]
    self.assertTrue(messages_count == 1)

  def test_load_posts(self):
    fbetl = Fbetl('tests/facebook-user')
    fbetl.load_posts()

    posts_count = fbetl.sql('SELECT COUNT(*) FROM posts;')[0][0]
    self.assertTrue(posts_count == 3)

if __name__ == '__main__':
    unittest.main()
