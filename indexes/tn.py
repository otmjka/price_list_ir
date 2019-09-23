import collections
import json
from logging import info
from helpers.tn import sku_str_to_dict
from db.common import get_term_docs_table, rw_term_docs_table

SPACE = ' '
COMMA = ','

"""
build_index_row_en_uuid - list [(id, data, row_num), ...] => sorted dict {[row_num]: en_uuid}

"""


##
## Indexes
##

"""
@param src - list [(id, data, row_num), ...]

@return sorted dict {[row_num]: en_uuid}

"""
def build_index_row_en_uuid(src):
  info('[+] build_index_row_en_uuid {[row_num]: en_uuid}')
  l = len(src)
  ROW_NUM_COL = 2
  start = src[0][ROW_NUM_COL]
  info('index starts with: [{}, ..., {}]'.format(start, l))
  idx = dict([(row_num, id) for id, data, row_num in src])
  return idx

# in given token_dict: dict
# create keys(term) if not exists
# append to term's docs list
def bow_to_dict(docid: int, trade_name: str, token_dict: dict, token_trade_name: dict):
  bow = set(trade_name.split(SPACE))
  for token in bow:
    if token in token_dict:
      if trade_name not in token_trade_name[token]:
        token_trade_name[token].append(trade_name)
      docid_list = token_dict[token]
      if docid in docid_list:
        continue
      docid_list.append(docid)
      sorted_list = sorted(docid_list)
      token_dict[token] = sorted_list

    else:
      docid_list = [docid]
      token_dict[token] = docid_list
      token_trade_name[token] = [trade_name]

# loads index from DB
def load_dict():
  recs = get_term_docs_table()
  l = len(recs)
  if l == 0:
    info('load_dict: term_docs is EMPTY')
    return False
  info('load_dict: {} terms'.format(l))
  term_docs_list = []
  token_trade_name_list = []
  term_keys = []

  for term, docs_json, trade_name in recs:
    doc_str = docs_json.split(COMMA)
    docs_ints = [int(s) for s in doc_str]
    term_keys.append(term)
    term_docs_list.append((term, docs_ints))
    token_trade_name_list.append((term, trade_name))

  term_docs_dict = dict(term_docs_list)
  token_trade_name = dict(token_trade_name_list) # TODO:
  # idx loaded. flag means do not save
  flag_save = False
  return term_docs_dict, token_trade_name, term_keys, flag_save

def save_tn_dict(token_doc_id: dict):
  info('prepare td_dict to save')
  keys = sorted(token_doc_id.keys())
  to_save = []
  for key in keys:
    term = key.replace("'", "''")
    int_to_str = ['{}'.format(n) for n in token_doc_id[key]]
    csv = ','.join(int_to_str)
    to_save.append((term, csv))
  if len(to_save) == 0:
    return False
  rw_term_docs_table(to_save)
  info('td_dict saved')
  return True

def compute_tn_index(src):
  info('start compute `term`: [doc_0, ...] index')
  TN_FIELD = 'trade_name'
  token_doc_id = dict()
  token_trade_name = dict()
  for id, sku_data_str, row_num in src:
    sku = json.loads(sku_data_str)
    trade_name = sku[TN_FIELD]
    bow_to_dict(row_num, trade_name, token_doc_id, token_trade_name)
  token_keys = sorted(token_doc_id.keys())
  info('TN dict created')
  return token_doc_id, token_trade_name, token_keys

def build_tn_dict(src):
  # try to load index or compute new one
  token_docs, token_tn, token_keys = load_dict() and compute_tn_index(src)
  save_tn_dict(token_docs, token_tn, token_keys)
  return token_docs, token_tn, token_keys

def build_indexes(src):
  info('\n\n##\n## Indexes\n##\n\nbuild indexes:')
  row_id = build_index_row_en_uuid(src)
  token_docs, token_tn, token_keys = build_tn_dict(src)
  return row_id, token_docs, token_tn, token_keys
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
