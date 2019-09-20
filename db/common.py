import sqlite3

def db_con(db_path):
  conn = sqlite3.connect(db_path, check_same_thread=False, uri=True)
  cursor = conn.cursor()
  return conn, cursor

def is_table_exists(table_name, cursor):
  query = "SELECT name FROM sqlite_master WHERE type='table' AND name='{}';".format(table_name)
  cursor.execute(query)
  result = cursor.fetchall()
  return len(result) > 0

def create_row_en_id_table(conn, cursor):
  if is_table_exists('row_en_id', cursor):
    return
  cursor.execute(
    'CREATE TABLE row_en_id (id text, row_num int PRIMARY KEY ASC)'
  )
  conn.commit()


fn_db = '/Users/admin/projects/pharm-portal/syn-py/src/bin/generated-2019-07-29/syn.db'

conn, cursor = db_con(fn_db)
create_row_en_id_table(conn, cursor)

print('[+] setup: connect to sqlite')
print('[+] setup: create table row_en_id')

def get_en_skus():
  print('[+] 1. get_en_skus')
  print('[+] 1.1 fetch ISKUS')
  query = 'select id, data, row_num from ISKUs order by row_num'
  cursor.execute(query)
  result = cursor.fetchall()
  return result

def save_idx_row_id(idx):
  batch = 1000
  print('save_idx_row_id')

def save_tn_dict(tn_term_dict):
  print('save_tn_dict')

def load_tn_term_dict():
  print('load_tn_term_dict')
  return []