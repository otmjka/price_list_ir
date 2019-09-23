from logging import info
import sqlite3

# TODO: is module init happends once?
# TODO: remove to config
DB_PATH = '/Users/admin/projects/pharm-portal/syn-py/src/bin/generated-2019-07-29/syn.db'

TN_TERM_DOCS = 'term_docs'
TN_ROW_ID = 'row_en_id'
TN_UN = 'ISKUs'
# exists table flag
row_en_id_exist = False

info('db: init {}'.format(DB_PATH))

# cached TN_ROW_ID {[row_num]: en_uuid}
# un_skus = None
cache = dict(un_skus=None)

def db_con(db_path):
  info('connecting to {}'.format(db_path))
  conn = sqlite3.connect(db_path, check_same_thread=False, uri=True)
  cursor = conn.cursor()
  info('connected')
  return conn, cursor

#
# Init module. first import.
#

conn, cursor = db_con(DB_PATH)

#
# Common
#
def is_table_exists(table_name, cursor=cursor):
  q = 'SELECT name FROM sqlite_master WHERE type=\'table\' AND name=\'{}\';'
  query = q.format(table_name)
  cursor.execute(query)
  records = cursor.fetchall()
  result = len(records) > 0
  info('is table `{}` exists?: {}'.format(table_name, result))
  return result

def truncate_table(table_name, rw=False, conn=conn, cursor=cursor):
  # TODO:
  if rw == True:
    q = 'DELETE FROM {};'
    query = q.format(table_name)
    cursor.execute(query)
    conn.commit()
#
# Create tables
#
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
  q = 'CREATE TABLE {} (term TEXT PRIMARY KEY ASC, docs_json TEXT)'
  query = q.format(TN)
  cursor.execute(query)
  conn.commit()
  info('table `{}` was create[{}]'.format(TN, query))


create_row_en_id_table()
create_tn_term_docs_table()

def save_tn_dict(tn_term_dict):
  print('save_tn_dict')

def load_tn_term_dict():
  print('load_tn_term_dict')
  return []