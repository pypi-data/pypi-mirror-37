from fbetl.extractors.extractor import Extractor

class Reactions(Extractor):
  def __init__(self, db, path):
    super().__init__(db, path)

  def create_table(self):
    self.sql('''
      CREATE TABLE reactions(
        title     TEXT NOT NULL,
        reaction  TEXT NOT NULL,
        timestamp DATETIME NOT NULL
      );
    ''')

  def load(self):
    data = self.load_json('/likes_and_reactions/posts_and_comments.json')

    for raw_reaction in data['reactions']:
      timestamp = self.extract_time(raw_reaction['timestamp'])
      title     = self.sql_safe(raw_reaction['title'])
      reaction  = raw_reaction['data'][0]['reaction']['reaction']

      self.sql(f'''
        INSERT INTO reactions (
          title,
          reaction,
          timestamp
        ) VALUES (
          '{title}',
          '{reaction}',
          '{timestamp}'
        );
      ''')

    self.db.commit()
