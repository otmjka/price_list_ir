from collections import OrderedDict
from logging import info

import db.un as db_un
import db.tn as db_tn

from helpers.strings import get_bow
from enums.common import COMMA


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
  return term_docs_dict

"""
# side effect, mutate given @param terms_docs
# create keys of @param `trade_name` if not exists
# append doc item to term docs list of trade_name term
# @params terms_docs: OrderedDict {[term]: docs, ...}
"""
def bow_to_dict(docid: int, trade_name: str, terms_docs: OrderedDict):
  bow = get_bow(trade_name)
  # remove empty items
  bow = [t for t in bow if len(t) > 0]
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

def compute_tn_index(un_skus):
  info('start compute `term`: [doc_0, ...] index')
  TN_FIELD = 'trade_name'
  terms_docs_dict = dict()
  for row_num, (un_id, sku) in enumerate(un_skus):
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
    term_value = term[0]
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
def build_tn_indexes():
  info('\n\n##\n## Indexes\n##\n\nbuild `trade_name` indexes:')

  terms_docs = build_tn_dict() # ordered dict {[term]: [doc_id_0, ..., doc_id_n]}
  return dict(terms_docs=terms_docs)

def add_to_tn_index(term, doc, terms_docs):
  # get existing item or new list
  term_docs = term in terms_docs and terms_docs[term] or list()
  if doc in term_docs:
    return print('there is a doc[{}] in term[{}]'.format(doc, term))
  # can optimizate, where insert?
  term_docs.append(doc)
  newdocs = sorted(term_docs)
  terms_docs[term] = newdocs
