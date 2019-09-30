import re

import db.un as db_un
from db.un import get_en_skus
from db.dosage import fetch_dosage_forms

from indexes.skus import build_sku_row_idx

from helpers.skus import str_to_dict
from helpers.strings import get_bow

from enums.common import MAN_FORMS, DOSAGE_FORM_ID

# {
# ...
#   ['bc479032-5c43-4f32-a98f-e020fcb77f1d']: {
#     'name': 'вспомогательное вещество-капсулы целлюлозные №00',
#     'docs': {46077, 47318}
#   }
# ...
# }
def get_dosage_items():
  skus = db_un.get_en_skus()
  dosages = dict() # {[id]: value}

  for un_id, data_str, row_num in skus:
    sku_data = str_to_dict(data_str)
    man_forms = sku_data['man_forms']
    for man_form in man_forms:
      dosage_form = man_form['dosage_form']
      name = dosage_form['name']
      dosage_id = dosage_form['id']
      if dosage_id not in dosages:
        dosages[dosage_id] = dict(name=name)
      if 'docs' not in dosages[dosage_id]:
        dosages[dosage_id]['docs'] = set()
      docs = dosages[dosage_id]['docs']
      docs.add(row_num)
  return dosages

# m = 0
# m = max(m, len(man_forms))
# print(m)
# => 5


# dosages_items = list(dosages.items())[:1000]
# dosages_items[245]
#
# # one_let = set()
# # two_let = set()
# three_let = set()
# for row, value in three:
#     print('{} `{}` [{}]'.format(row, value, dosages_items[row][1]['name']))
#     three_let.add(value)
# three_let
#
# ## 268 `el` [вспомогательное вещество-капсулы желатиновые твердые №0 el]
# # 600 `е1` [вспомогательное вещество-капсулы целлюлозные №0 е1]
# for row in dosages_items[529][1]['docs']:
#     print(skus[row][0])
#
def build_forms_idx():
  dosages_dict = get_dosage_items()
  dosages_items = list(dosages_dict.items())
  one = list()
  two = list()
  three = list()
  single_stop = {'в', 'и', 'с'}
  dual_stop = {'на', 'со'}
  for i, (form_id, form_dict) in enumerate(dosages_items):
    name = form_dict['name']
    docs = form_dict['docs']
    bag_of_words = re.split(
      r"\+|\|\*| |\n|\(|\)|\-|\[|\]|'|\"|\t|«|»|&|;|:|,",
      name
    )
    bow = list()
    for word in bag_of_words:
      if len(word) == 0: # ""
        continue
      # {'2', '4', 'в', 'и', 'с', '…'}
      # '4' 661 раствор для гемодиализа [калий 4 ммоль/л] ['раствор', 'для', 'гемодиализа', 'калий', '4', 'ммоль/л']
      # '2' 662 раствор для гемодиализа [калий 2 ммоль/л]
      # 245 `…` [порошок для приготовления …]
      if len(word) == 1:
        one.append((i, word))
        if word in single_stop:
            continue
      # {'el', 'е1', 'на', 'со', '№0', '№1', '№2', '№3', '№4'}
      # 268 `el` [вспомогательное вещество-капсулы желатиновые твердые №0 el]
      # 600 `е1` [вспомогательное вещество-капсулы целлюлозные №0 е1]
      if len(word) == 2:
        two.append((i, word))
        if word in dual_stop:
            continue
      # 529 `№00` [вспомогательное вещество-капсулы целлюлозные №00]
      if len(word) == 3:
        three.append((i, word))
      bow.append(word)
  #     bow = [word for word in bag_of_words if len(word) > 0]
    print('[{}] [{}]'.format(i, len(docs)))
    print('{}\n{}\n{}\n\n'.format(name, bag_of_words, bow))


#
# updated indexes
#

def get_row_id_idx(recs):
  return dict([(i, r[0]) for i, r in enumerate(recs)])


def get_id_row_idx(recs):
  return dict([(r[0], i) for i, r in enumerate(recs)])

# => {term:[company_id]}
def build_terms_docs(items, id_row_idx, term_dict={}):
  for dosage_form_id, name, _ in items:
    i = id_row_idx[dosage_form_id] # get 0..n doc index
    bow = get_bow(name)

    for term in bow:
      if term not in term_dict:
        term_dict[term] = []
      docs = term_dict[term]
      if i in docs:
        continue
      docs.append(i)
      docs = sorted(docs)
      term_dict[term] = docs
  return term_dict

def build_dosage_forms_idx():
  recs = fetch_dosage_forms()
  row_id_idx = get_row_id_idx(recs)
  id_row_idx = get_id_row_idx(recs)

  terms_docs = build_terms_docs(recs, id_row_idx)
  return dict(terms_docs=terms_docs,
              row_id=row_id_idx,
              id_row=id_row_idx)

#
# UN's skus table
#

def get_sku_uuid(sku: tuple):
  return sku[0]


def get_sku_data(sku: tuple):
  return sku[1]


def get_dosage_form_id(sku_data: dict):
  man_forms = sku_data[MAN_FORMS]
  dosage_id_list = [mform[DOSAGE_FORM_ID] for mform in man_forms]
  #     dosage_id = man_forms[DOSAGE_FORM_ID]
  return dosage_id_list


### go through UN skus table
### => {.., [${dosage_row}]: [sku_doc_0, ..., sku_doc_n], ...}
def build_dosage_row_docs(skus, skus_id_rows_idx, dosage_forms_idx):
  dosage_row_id = dosage_forms_idx['id_row']
  row_docs = dict()
  for sku in skus:
    un_id = get_sku_uuid(sku)  # 00004ee5-aea0-4fb4-9d0b-a401584c6be5
    sku_data = get_sku_data(sku)  # {"packs": {}, ..., "trade_name": "...", "address_id": "..."}
    # doc_row by un_sku_id
    un_sku_idx = skus_id_rows_idx[un_id]  # => 0 ; {..., [`${un_id}`]: row_num, ...}
    dosage_id_list = get_dosage_form_id(sku_data)  # get sku.address_id == for ==> company_id
    for dosage_id in dosage_id_list:
      # TODO: check existence
      if dosage_id not in dosage_row_id:
        print('fail address id {}\n sku: [{}]{}'.format(dosage_id, un_sku_idx, un_id))
        continue

      dosage_row_by_id = dosage_row_id[dosage_id]

      # build dictionary
      # row_num: docs_rows
      docs = dosage_row_by_id in row_docs and row_docs[dosage_row_by_id] or list()

      if un_sku_idx not in docs:
        docs.append(un_sku_idx)
        docs = sorted(docs)

      row_docs[dosage_row_by_id] = docs
  return row_docs

def get_dosage_row_docs():
  # sku index
  un_skus = get_en_skus()
  sku_indexes = build_sku_row_idx()
  skus_id_rows_idx = sku_indexes['rows_id_inv']

  # dosage index
  # => 'terms_docs', 'row_id', 'id_row'
  dosage_forms_idx = build_dosage_forms_idx()
  row_docs = build_dosage_row_docs(un_skus, skus_id_rows_idx, dosage_forms_idx)
  return row_docs




