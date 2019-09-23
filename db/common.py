from logging import info
import sqlite3


TN_TERM_DOCS = 'term_docs'
TN_ROW_ID = 'row_en_id'

def db_con(db_path):
  info('connecting to {}'.format(db_path))
  conn = sqlite3.connect(db_path, check_same_thread=False, uri=True)
  cursor = conn.cursor()
  info('connected')
  return conn, cursor

#
# Init module. first import.
#

# TODO: is init happend once?
fn_db = '/Users/admin/projects/pharm-portal/syn-py/src/bin/generated-2019-07-29/syn.db'
info('db: init {}'.format(fn_db))

conn, cursor = db_con(fn_db)

def is_table_exists(table_name, cursor=cursor):
  q = 'SELECT name FROM sqlite_master WHERE type=\'table\' AND name=\'{}\';'
  query = q.format(table_name)
  cursor.execute(query)
  records = cursor.fetchall()
  result = len(records) > 0
  info('is table `{}` exists?: {}'.format(table_name, result))
  return result

def create_row_en_id_table(conn=conn, cursor=cursor):
  TN = TN_ROW_ID
  if is_table_exists(TN, cursor):
    return
  q = 'CREATE TABLE {} (id text, row_num int PRIMARY KEY ASC)'
  query = q.format(TN)
  cursor.execute(query)
  conn.commit()
  info('table `{}` was created'.format(TN))

def create_tn_term_docs_table(conn=conn, cursor=cursor):
  TN = TN_TERM_DOCS
  if is_table_exists(TN, cursor):
    return
  q = 'CREATE TABLE {} (term TEXT PRIMARY KEY ASC, docs_json TEXT, trade_name TEXT)'
  query = q.format(TN)
  cursor.execute(query)
  conn.commit()
  info('table `{}` was create'.format(TN))


create_row_en_id_table()
create_tn_term_docs_table()

def get_en_skus():
  info('[+] 1. get_en_skus: load UN skus id, data, row_num')
  query = 'select id, data, row_num from ISKUs order by row_num'
  cursor.execute(query)
  result = cursor.fetchall()
  info('loaded records: {}'.format(len(result)))
  return result

def get_term_docs_table(conn=conn, cursor=cursor):
  q = 'select term, docs_json, trade_name from {} order by term'
  query = q.format(TN_TERM_DOCS)
  cursor.execute(query)
  records = cursor.fetchall()
  info('loaded records: {}'.format(len(records)))
  return records

def rw_term_docs_table(items, conn=conn, cursor=cursor):
  tn = TN_TERM_DOCS

  q = 'DELETE FROM {};'
  query = q.format(tn)
  cursor.execute(query)
  conn.commit()

  values = ['(\'{}\',\'{}\')'.format(term, docs_json) for term, docs_json in items]
  values = ','.join(values)

  q = 'INSERT INTO {} VALUES {};'
  query = q.format(tn, values)
  cursor.execute(query)
  conn.commit()

def save_idx_row_id(idx):
  batch = 1000
  print('save_idx_row_id')

def save_tn_dict(tn_term_dict):
  print('save_tn_dict')

def load_tn_term_dict():
  print('load_tn_term_dict')
  return []