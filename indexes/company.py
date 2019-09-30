from db.company import get_companies, get_companies_synonyms
from db.company import get_addr_company_table
# UN skus for indexing
from db.un import get_en_skus
from db.un import get_sku_uuid, get_sku_data

from indexes.skus import build_sku_row_idx

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
def build_skus_by_company_row():

  #
  # sku idx
  #

  un_skus = get_en_skus()

  sku_indexes = build_sku_row_idx()
  skus_id_rows_idx = sku_indexes['rows_id_inv']  # {..., [`${un_id}`]: row_num, ...}

  #
  # company
  #

  company_idx = build_company_idx()
  company_id_idx = company_idx['company_id_idx']

  addr_company_idx = get_addr_company_table()

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