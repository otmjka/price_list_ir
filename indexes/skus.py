from collections import OrderedDict
from logging import info

import db.un as db_un

"""
build_index_row_en_uuid - list [(id, data, row_num), ...] => sorted dict {[row_num]: en_uuid}

"""

def prepare_row_id_from_db(db_idx: list):
  return OrderedDict(db_idx)

def compute_row_id_idx(un_db, start=0):
  info('compute ordered dict {[row_num]: en_uuid}')
  l = len(un_db)
  info('index bounds: [{}, ..., {}]'.format(start, l))
  # `un_db` is supposed to be sorted by `row_num`
  db_idx = [(i, rec[0]) for i, rec in enumerate(un_db)]
  idx = prepare_row_id_from_db(db_idx)
  return idx

"""
# @fn build_index_row_en_uuid()
# @return sorted dict {[row_num]: en_uuid}
"""
def build_index_row_en_uuid():
  info('[+] build_index_row_en_uuid {[row_num]: en_uuid}')
  db_idx = db_un.load_row_un_id_index()
  # case: index cached in db
  if db_idx != False:
    idx = prepare_row_id_from_db(db_idx)
    return idx

  # case: there is no index cached in db
  un_db = db_un.get_en_skus()
  idx = compute_row_id_idx(un_db)
  db_un.save_row_id_idx(idx)

  return idx

# {[row_num]: UN_UUID} => {[UN_UUID]: row_num}
def build_inv_row_en_uuid(d: OrderedDict):
  items = list(d.items())
  id_row = dict([(un_id, row_num) for row_num, un_id in items])
  return id_row

def build_sku_row_idx():
  rows_id = build_index_row_en_uuid() # {[row_num]: UN_UUID}
  rows_id_inv = build_inv_row_en_uuid(rows_id) # {[UN_UUID]: row_num}
  return dict(rows_id=rows_id, rows_id_inv=rows_id_inv)


