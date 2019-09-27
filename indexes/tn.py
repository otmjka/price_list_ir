from collections import OrderedDict
import json
from logging import info
from helpers.tn import sku_str_to_dict
import db.un as db_un
import db.tn as db_tn


SPACE = ' '
COMMA = ','

"""
build_index_row_en_uuid - list [(id, data, row_num), ...] => sorted dict {[row_num]: en_uuid}

"""


##
## Indexes
##

def prepare_row_id_from_db(db_idx: list):
  return OrderedDict(db_idx)

def compute_row_id_idx(un_db):
  info('compute ordered dict {[row_num]: en_uuid}')
  ROW_NUM_COL = 2
  l = len(un_db)
  start = un_db[0][ROW_NUM_COL]
  info('index bounds: [{}, ..., {}]'.format(start, l))
  # `un_db` is supposed to be sorted by `row_num`
  db_idx = [(row_num, uuid) for uuid, _, row_num in un_db]
  idx = prepare_row_id_from_db(db_idx)
  return idx

"""
# @fn build_index_row_en_uuid()
# @param src - list [(id, data, row_num), ...]
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
def build_inv_row_en_uuid(d):
  items = list(d.items())
  id_row = dict([(un_id, row_num) for row_num, un_id in items])
  return id_row

"""
# loads index from DB
# if need make new one index
# => False 
# if exists in db cache
# => OrderDict, False
"""
def load_terms_docs_idx():
  recs = db_tn.get_term_docs_table()
  l = len(recs)
  if l == 0:
    info('load_dict: term_docs is EMPTY')
    return False
  info('load_dict: {} terms'.format(l))
  term_docs_list = []

  for term, docs_json in recs:
    doc_str = docs_json.split(COMMA)
    docs_ints = [int(s) for s in doc_str]
    term_docs_list.append((term, docs_ints))

  term_docs_dict = OrderedDict(term_docs_list)
  # idx loaded. flag means do not save
  flag_save = False
  return term_docs_dict

"""
# in given token_dict: dict
# create keys(term) if not exists
# append to term's docs list
"""
def bow_to_dict(docid: int, trade_name: str, terms_docs: dict):
  bow = set(trade_name.split(SPACE))
  for term in bow:
    if term in terms_docs:
      docid_list = terms_docs[term]
      if docid in docid_list:
        continue
      docid_list.append(docid)
      sorted_list = sorted(docid_list)
      terms_docs[term] = sorted_list

    else:
      docid_list = [docid]
      terms_docs[term] = docid_list


def compute_tn_index(un_db):
  info('start compute `term`: [doc_0, ...] index')
  TN_FIELD = 'trade_name'
  terms_docs_dict = dict()
  for id, sku_data_str, row_num in un_db:
    sku = json.loads(sku_data_str)
    trade_name = sku[TN_FIELD]
    bow_to_dict(row_num, trade_name, terms_docs_dict)
  token_keys = sorted(terms_docs_dict.keys())
  sorted_terms_docs_list = [(term, terms_docs_dict[term]) for term in token_keys]
  terms_docs = OrderedDict(sorted_terms_docs_list)
  info('TN dict created')
  return terms_docs

def save_tn_dict(terms_docs_idx: OrderedDict):
  info('prepare td_dict to save')
  to_save = []
  for term in terms_docs_idx.items():
    term_value = term[0].replace("'", "''")
    docid_list = term[1]
    int_to_str = ['{}'.format(n) for n in docid_list]
    csv = ','.join(int_to_str)
    to_save.append((term_value, csv))
  if len(to_save) == 0:
    return False
  # save index
  db_tn.save_term_docs_table(to_save)
  info('td_dict saved')
  return True

def build_tn_dict():
  # try to load index or compute new one
  terms_docids = load_terms_docs_idx()
  if terms_docids != False:
    return terms_docids

  un_db_skus = db_un.get_en_skus()
  terms_docids = compute_tn_index(un_db_skus)

  save_tn_dict(terms_docids)
  return terms_docids

# build {[row_num]: UN_UUID} dict
# build ordered dict {[term]: [doc_id_0, ..., doc_id_n]}
def build_indexes():
  info('\n\n##\n## Indexes\n##\n\nbuild indexes:')
  rows_id = build_index_row_en_uuid() # {[row_num]: UN_UUID}
  rows_id_inv = build_inv_row_en_uuid(rows_id)
  terms_docs = build_tn_dict() # ordered dict {[term]: [doc_id_0, ..., doc_id_n]}
  return dict(rows_id=rows_id,
              terms_docs=terms_docs,
              rows_id_inv=rows_id_inv)

##
## select documens by term
##
def get_terms_skus(bow, d):
  print('get_terms_skus: input bow, for each looking for skus')
  return []

##
## intersection
##
def intersection(list_terms_skus):
  print('intersection')
  result = []
  return result
