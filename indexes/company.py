from db.company import get_companies, get_companies_synonyms
# UN skus for indexing
from db.un import get_sku_uuid, get_sku_data

from helpers.strings import get_bow


# @params items [(company_id, name),...]
# => {company_id: row_num}
def build_id_row_idx(items):
  company_id_idx = dict()
  for i, (company_id, _) in enumerate(items):
    company_id_idx[company_id] = i
  return company_id_idx


# => {term:[company_id]}
def build_terms_docs(items, company_id_idx, term_dict={}):
  for company_id, name in items:
    i = company_id_idx[company_id] # get 0..n doc index
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

def to1(no, nr, nrs):
  return '{} {} {}'.format(no != None and no or '',
                           nr != None and nr or '',
                           nrs != None and nrs or '')

# => [(company_id, name)]
def norm_companies(companies):
  # no, nr, nrs - origin, rus, rus_short
  c_norm = [(company_id, to1(no, nr, nrs)) for company_id, no, nr, nrs in companies]
  return c_norm

# =>
# {
#   company_id_idx: {[company_id]: row_num},
#   terms_docs: {[term]: [company_doc, ...]}
# }
def build_company_idx():
  c_raw = get_companies()  # [id, name1, name2, name3]
  c = norm_companies(c_raw)  # [id, name]
  company_id_idx = build_id_row_idx(c)  # {company_id: row_num}
  """
  ### => {row_num: company_id} =+> [company_id]
  """
  company_id_idx_inv = dict([(row, c_id) for c_id, row in company_id_idx.items()])

  cs = get_companies_synonyms()  # [id, name]
  # ddd {term: [company_id, ...]}
  terms_docs = build_terms_docs(c, company_id_idx)
  terms_docs = build_terms_docs(cs, company_id_idx, terms_docs)
  # rep(ddd)
  return dict(company_id_idx=company_id_idx,
              company_id_idx_inv=company_id_idx_inv,
              terms_docs=terms_docs,
              companies_table=c_raw,
              companies_synonyms=cs)

# fail address id d8c7d99f-17e2-422e-a8dc-306fbb502483
#  sku: [46127]51c219b3-071c-47b0-bd2f-3ede6f091649
# fail address id d8c7d99f-17e2-422e-a8dc-306fbb502483
#  sku: [50758]59a60901-340c-49f6-a47a-f01ce772cde5
# fail address id d8c7d99f-17e2-422e-a8dc-306fbb502483
#  sku: [132135]eb196502-7f24-4580-8337-3efc531cd194

# aid = 'd8c7d99f-17e2-422e-a8dc-306fbb502483'
# cid = '5616c61a-d00c-4d09-a9ab-d847226bb3b3'

# add_to_company_idx(address_id=aid, company_id=cid, idx=addr_company_idx['addr_cmp'])
def add_to_company_idx(address_id, company_id, idx):
  idx[address_id] = company_id


# from un sku
def get_address_id(data: dict):
  return data['address_id']


### go through UN skus table
### create
### {..., [${company_row}]: [sku_doc_0, ..., sku_doc_n], ...}
def build_skus_by_company_row(idx):

  #
  # sku idx
  #

  un_skus = idx['un_skus']

  skus_id_rows_idx = idx['skus_idx']['rows_id_inv']  # {..., [`${un_id}`]: row_num, ...}

  #
  # company
  #

  company_idx = idx['company_idx']
  company_id_idx = company_idx['company_id_idx']

  addr_company_idx = idx['addr_company_idx']

  # build_skus_by_company_row output:
  # fail address id d8c7d99f-17e2-422e-a8dc-306fbb502483
  #  sku: [46127]51c219b3-071c-47b0-bd2f-3ede6f091649
  # fail address id d8c7d99f-17e2-422e-a8dc-306fbb502483
  #  sku: [50758]59a60901-340c-49f6-a47a-f01ce772cde5
  # fail address id d8c7d99f-17e2-422e-a8dc-306fbb502483
  #  sku: [132135]eb196502-7f24-4580-8337-3efc531cd194

  aid = 'd8c7d99f-17e2-422e-a8dc-306fbb502483'
  cid = '5616c61a-d00c-4d09-a9ab-d847226bb3b3'

  add_to_company_idx(address_id=aid, company_id=cid, idx=addr_company_idx['addr_cmp'])
  company_id_by_address = addr_company_idx['addr_cmp']

  row_docs = dict()
  for sku in un_skus:
    un_id = get_sku_uuid(sku)  # 00004ee5-aea0-4fb4-9d0b-a401584c6be5
    sku_data = get_sku_data(sku)  # {"packs": {}, ..., "trade_name": "...", "address_id": "..."}
    # doc_row by un_sku_id
    un_sku_idx = skus_id_rows_idx[un_id]  # => 0 ; {..., [`${un_id}`]: row_num, ...}
    address_id = get_address_id(sku_data)  # get sku.address_id == for ==> company_id
    if address_id not in company_id_by_address:
      print('fail address id {}\n sku: [{}]{}'.format(address_id, un_sku_idx, un_id))
      continue
    company_id = company_id_by_address[address_id]  # address_id => company_id
    company_row_by_id = company_id_idx[company_id]  # company_id => row_company_id

    # build dictionary
    # row_num: docs_rows
    docs = company_row_by_id in row_docs and row_docs[company_row_by_id] or list()

    if un_sku_idx not in docs:
      docs.append(un_sku_idx)
      docs = sorted(docs)

    row_docs[company_row_by_id] = docs
  return row_docs


def company_short_name(sku_data, idx: dict):
  address_id = get_address_id(sku_data)

  company_idx = idx['company_idx']
  addr_company_idx = idx['addr_company_idx']
  company_id_by_address_id = addr_company_idx['addr_cmp']
  company_id = company_id_by_address_id[address_id]

  company_id_idx = company_idx['company_id_idx']
  c_row = company_id_idx[company_id]

  short_rus_name = get_company_sname(c_row, idx)
  return short_rus_name

def get_company_sname(cdoc: int, idx: dict):
  company_idx = idx['company_idx']
  company_src = company_idx['companies_table']
  c_rec = company_src[cdoc]
  short_rus_name = c_rec[3] or c_rec[2] or c_rec[1]
  return short_rus_name

# sku_data => address_id => company_id => company_row
def get_company_row_by_sku_data(sku_data, idx):
  address_id = get_address_id(sku_data)
  company_id = idx['addr_company_idx']['addr_cmp'][address_id]
  company_row = idx['company_idx']['company_id_idx'][company_id]
  return company_row

def add_terms_docs(term_str, doc, idx):
  terms_docs = idx['company_idx']['terms_docs']
  terms = get_bow(term_str)
  for t in terms:
    if t not in terms_docs:
      terms_docs[t] = list()
    docs = terms_docs[t]
    if doc in docs:
      print('{} exists in {} skipped'.format(doc, t))
      continue
    docs.append(doc)
    terms_docs[t] = sorted(docs)