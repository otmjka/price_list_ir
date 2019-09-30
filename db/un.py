from logging import info

from db.common import TN_UN, TN_ROW_ID
from db.common import conn, cursor, cache
from db.skus import un_db_conn

def load_row_un_id_index(cursor=cursor):
  info('[+] 1. get_en_skus: load UN skus id, data, row_num')
  q = 'select row_num, id from {} order by row_num'
  query = q.format(TN_ROW_ID)
  cursor.execute(query)
  records = cursor.fetchall()
  l = len(records)
  if l > 0:
    info('row_un_id: loaded records: {}'.format(l))
    return records
  return False

# TODO: at first load: str to dict
# TODO: simple index where trade_name, count and etc in completed form
#
# UN data
#
def get_en_skus():
  # check cache
  un_skus = cache['un_skus']
  if un_skus != None:
    return un_skus
  info('[+] 1. get_en_skus: load UN skus id, data, row_num')

  conn, cursor, = un_db_conn()
  q = 'select id, data from skus as s order by id;'
  query = q.format(TN_UN)
  cursor.execute(query)
  result = cursor.fetchall()
  conn.close()
  cache['un_skus'] = result
  info('loaded records: {}'.format(len(result)))
  return result

# TODO: check for duplicates indexes/forms
def get_sku_uuid(sku: tuple):
  return sku[0]

# TODO: check for duplicates
def get_sku_data(sku: tuple):
  return sku[1]

def save_row_id_idx(idx, conn=conn, cursor=cursor, rw=True):
  tn = TN_ROW_ID
  # TODO: separate fn
  # truncate table
  if rw == True:
    q = 'DELETE FROM {};'
    query = q.format(tn)
    cursor.execute(query)
    conn.commit()
  #
  items = idx.items()
  values = ['(\'{}\',\'{}\')'.format(un_id, row_num) for row_num, un_id in items]
  values = ','.join(values)

  q = 'INSERT INTO {} VALUES {};'
  query = q.format(tn, values)
  cursor.execute(query)
  conn.commit()
