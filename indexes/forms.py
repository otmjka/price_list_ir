import re

import db.un as db_un
from db.un import get_en_skus
from db.dosage import fetch_dosage_forms

from indexes.skus import build_sku_row_idx

import json
from helpers.strings import get_bow

from enums.common import MAN_FORMS, DOSAGE_FORM_ID


def dosage_name_by_id(dosage_id, idx):
  dosage_idx = idx['dosage_idx']
  dosage_id_row = dosage_idx['id_row']
  dosage_forms_recs = dosage_idx['recs']
  dosage_row = dosage_id_row[dosage_id]
  dosage_rec = dosage_forms_recs[dosage_row]
  dosage_name = dosage_rec[1]
  return dosage_name


def dosage_rows_by_id_list(dosage_id_list, idx):
  dosage_idx = idx['dosage_idx']
  dosage_id_row = dosage_idx['id_row']
  dosage_rows = [dosage_id_row[dosage_id] for dosage_id in dosage_id_list]
  return dosage_rows

def dosage_names_by_id_list(dosage_id_list, idx):
  dosage_names = list()
  for dosage_id in dosage_id_list:
    dosage_name = dosage_name_by_id(dosage_id, idx)
    dosage_names.append(dosage_name)
  return dosage_names
# {
# ...
#   ['bc479032-5c43-4f32-a98f-e020fcb77f1d']: {
#     'name': 'вспомогательное вещество-капсулы целлюлозные №00',
#     'docs': {46077, 47318}
#   }
# ...
# }
def str_to_dict(sku_str: str):
  sku_dict = json.loads(sku_str)
  return sku_dict

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
              id_row=id_row_idx,
              recs=recs)

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
  return dosage_id_list

def get_dosage_names(sku_data, idx):
  dosage_id_list = get_dosage_form_id(sku_data)
  dosage_names = dosage_names_by_id_list(dosage_id_list, idx)
  return dosage_names

def get_dosage_rows(sku_data, idx):
  dosage_id_list = get_dosage_form_id(sku_data)
  dosage_rows = dosage_rows_by_id_list(dosage_id_list, idx)
  return dosage_rows

### go through UN skus table
### => {.., [${dosage_row}]: [sku_doc_0, ..., sku_doc_n], ...}
def build_dosage_row_docs(idx):
  # sku index
  un_skus = idx['un_skus']
  skus_id_rows_idx = idx['skus_idx']['rows_id_inv']
  dosage_row_id = idx['dosage_idx']['id_row']

  row_docs = dict()
  for sku in un_skus:
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

# ('0006df9c-f765-4821-82f0-0f5dd6b28126', 'лиофилизат спрея', '13.3')
def get_dosage_by_row(doc, idx):
    dosage_forms_recs = idx['dosage_idx']['recs']
    dosage_rec = dosage_forms_recs[doc]
    uuid, name, code = dosage_rec
    return name

def get_dosage_row_docs(idx):

  # dosage index
  # => 'terms_docs', 'row_id', 'id_row'
  row_docs = build_dosage_row_docs(idx)
  return row_docs

def get_dosage_row_by_un_id(un_id, idx):
  skus_id_row_idx = idx['skus_idx']['rows_id_inv']
  un_skus = idx['un_skus']
  sku_row_number = skus_id_row_idx[un_id]
  sku_data = un_skus[sku_row_number][1]
  dosage_id_list = get_dosage_form_id(sku_data)
  dosage_names = dosage_names_by_id_list(dosage_id_list, idx)
  dosage_rows = dosage_rows_by_id_list(dosage_id_list, idx)
  return dosage_rows, dosage_names

#
# verifed
#

# из верифицированных берем чтоб добавить в словарь
def get_verified_dosage_by_row(price_row, verified, idx):
  un_id = verified[price_row]
  dosage_rows, dosage_names = get_dosage_row_by_un_id(un_id, idx)
  print(dosage_rows, dosage_names)
  return dosage_rows, dosage_names

# добавляет дозировку из верифицированного документа
def add_dosage_term_list_doc(terms, verified_row, verified, idx):
  terms_docs = idx['dosage_idx']['terms_docs']
  # [1225] ['таблетки, покрытые оболочкой']
  dosage_docs, dosage_names = get_verified_dosage_by_row(verified_row, verified, idx)

  for t in terms:
    if t not in terms_docs:
      print('[{}] not exists!'.format(t))
      terms_docs[t] = list()
    docs = terms_docs[t]
    for ddoc in dosage_docs:
      if ddoc in docs:
        print('{} exists in {} skipped'.format(ddoc, t))
        continue
      docs.append(ddoc)
      terms_docs[t] = sorted(docs)

"""
### from indexes.forms import build_dosage_row_docs
### # by dosage row get all docs(skus) where meeted
### skus_by_dosage_row = build_dosage_row_docs(idx)
### idx['skus_by_dosage_row'] = skus_by_dosage_row
"""

