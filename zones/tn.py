from helpers.strings import get_bow
from helpers.skus import get_tn

"""
### { `term`: [sku_doc_0, ...], ...}
###
###

### TODO: term -> trade term-source
"""
def tn_zone(sku_name, terms_docs):
  zone = list()
  name_terms = get_bow(sku_name)
  for term in name_terms:
    docs = None
    if term in terms_docs:
      docs = terms_docs[term]
    zone.append((term, docs))
  return zone

def tn_zone(sku_name, terms_docs):
  name_terms = get_bow(sku_name)
  return [(term, terms_docs.get(term, None)) for term in name_terms]

def test_tn_item(item):
    # all tn equal
    # single word
#     print('\n!',item[0][0][1], '\n*')
    docs = item[0][0][1]
    if docs == None:
        return False
    tn_start = get_tn(docs[0])
    if len(tn_start.split(' ')) > 1:
        return False
    for doc in docs:
        tn_cur = get_tn(doc)
        if tn_cur != tn_start:
            return False
        tn_start = tn_cur
    return True


def through_tn_zone(live_imp):
  res = list()
  for code, sku_name, company in live_imp:
    tn_res = tn_zone(sku_name)
    if test_tn_item(tn_res):
      res.append((code, tn_res))
  return res
