from db.common import db_con, is_table_exists


UPLOADS_TABLE = 'uploads'
cached = dict()

def create_uploads_table(table_name=UPLOADS_TABLE, conn=None, cursor=None):
  if conn == None or cursor == None:
    conn, cursor = db_con()
  if is_table_exists(table_name):
    return False

  q = 'CREATE TABLE {} (hash text PRIMARY KEY ASC, path text)'
  query = q.format(table_name)
  cursor.execute(query)
  conn.commit()
  conn.close()

def save_to_uploads(items: list, conn=None, cursor=None):
  if conn == None or cursor == None:
    conn, cursor = db_con()
  tn = UPLOADS_TABLE
  values = ['(\'{}\',\'{}\')'.format(md5, fp) for fp, (md5, sha1) in items]
  values = ','.join(values)
  q = 'INSERT INTO {} VALUES {};'
  query = q.format(tn, values)
  cursor.execute(query)
  conn.commit()
  conn.close()

def load_uploads_list(conn=None, cursor=None):
  if conn == None or cursor == None:
    conn, cursor = db_con()

  if UPLOADS_TABLE in cached:
    return cached[UPLOADS_TABLE]

  q = 'select * from {};'
  query = q.format(UPLOADS_TABLE)
  cursor.execute(query)
  uploads_recs = cursor.fetchall()
  cached['UPLOADS_TABLE'] = uploads_recs
  return uploads_recs
