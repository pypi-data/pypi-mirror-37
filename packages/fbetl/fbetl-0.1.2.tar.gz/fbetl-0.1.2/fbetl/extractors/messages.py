from os import walk
from fbetl.extractors.extractor import Extractor

class Messages(Extractor):
  def __init__(self, db, path):
    super().__init__(db, path)

  def create_table(self):
    self.sql('''
      CREATE TABLE messages(
        sender_name TEXT NOT NULL,
        content     TEXT NOT NULL,
        title       TEXT NOT NULL,
        thread_path TEXT NOT NULL,
        type        TEXT NOT NULL,
        timestamp   DATETIME NOT NULL
      );
    ''')

  def load(self):
    message_threads_uri = '/messages/'
    message_threads = sorted(next(walk(self.path + message_threads_uri))[1])
    message_threads.remove('stickers_used')

    for message_thread in message_threads:
      data = self.load_json(message_threads_uri + message_thread + '/message.json')

      thread_path = self.sql_safe(data['thread_path'])
      title       = self.sql_safe(data.get('title', 'thread_path'))

      for message in data['messages']:
        sender_name = self.sql_safe(message.get('sender_name', ''))
        content     = self.sql_safe(message.get('content', ''))
        type        = message['type']
        timestamp   = self.extract_time(message['timestamp_ms'] / 1000.0)

        self.sql(f'''
          INSERT INTO messages (
            sender_name,
            content,
            title,
            thread_path,
            type,
            timestamp
          ) VALUES (
            '{sender_name}',
            '{content}',
            '{title}',
            '{thread_path}',
            '{type}',
            '{timestamp}'
          );
        ''')

    self.db.commit()
