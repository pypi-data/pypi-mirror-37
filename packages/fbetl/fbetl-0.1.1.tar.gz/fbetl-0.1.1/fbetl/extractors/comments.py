from fbetl.extractors.extractor import Extractor

class Comments(Extractor):
  def __init__(self, db, path):
    super().__init__(db, path)

  def create_table(self):
    self.sql('''
      CREATE TABLE comments(
        title     TEXT NOT NULL,
        text      TEXT,
        url       TEXT,
        uri       TEXT,
        timestamp DATETIME NOT NULL
      );
    ''')

  def load(self):
    data = self.load_json('/comments/comments.json')

    for raw_comment in data['comments']:
      comment = self.shape_comment(raw_comment)

      self.sql(f'''
        INSERT INTO comments (
          title,
          text,
          url,
          uri,
          timestamp
        ) VALUES (
          '{comment['title']}',
          '{comment.get('text', '')}',
          '{comment.get('url', '')}',
          '{comment.get('uri', '')}',
          '{comment['timestamp']}'
        );
      ''')

    self.db.commit()

  def shape_comment(self, raw_comment):
    comment = {}
    comment['title']     = self.sql_safe(raw_comment['title'])
    comment['timestamp'] = self.extract_time(raw_comment['timestamp'])

    if 'data' in raw_comment.keys():
      comment['text'] = self.sql_safe(raw_comment['data'][0]['comment'].get('comment')) or ''
    if 'attachments' in raw_comment.keys():
      for attachment in raw_comment['attachments'][0]['data']:
        if 'external_context' in attachment.keys():
          comment['url'] = attachment['external_context']['url']
        if 'media' in attachment.keys():
          comment['uri'] = attachment['media']['uri']

    return comment
