from fbetl.extractors.extractor import Extractor

class Posts(Extractor):
  def __init__(self, db, path):
    super().__init__(db, path)

  def create_table(self):
    self.sql('''
      CREATE TABLE posts(
        title     TEXT NOT NULL,
        post      TEXT NOT NULL,
        url       TEXT NOT NULL,
        photo     TEXT NOT NULL,
        timestamp DATETIME NOT NULL
      );
    ''')

  def load(self):
    data = self.load_json('/posts/your_posts.json')

    for status_update in data['status_updates']:
      timestamp = self.extract_time(status_update['timestamp'])
      title     = self.sql_safe(status_update.get('title', ''))

      try:
        post = self.sql_safe(status_update['data'][0]['post'])
      except KeyError:
        post = ''

      try:
        url  = self.sql_safe(status_update['attachments'][0]['data'][0]['external_context']['url'])
      except KeyError:
        url = ''

      try:
        photo  = status_update['attachments'][0]['data'][0]['media']['uri']
      except KeyError:
        photo = ''

      self.sql(f'''
        INSERT INTO posts (
          title,
          post,
          url,
          photo,
          timestamp
        ) VALUES (
          '{title}',
          '{post}',
          '{url}',
          '{photo}',
          '{timestamp}'
        );
      ''')

    self.db.commit()
