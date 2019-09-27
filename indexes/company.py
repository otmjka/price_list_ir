from db.company import get_companies, get_companies_synonyms
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
              terms_docs=terms_docs)