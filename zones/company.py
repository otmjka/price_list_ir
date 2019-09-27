from helpers.strings import get_bow

# for each plist line
# [[(term, [doc, ...]), ...],...]
def through_company_zone(plist_values, terms_docs):
  zone = list()
  for code, sku_name, company in plist_values:
    company_terms = get_bow(company)
    freq = list()
    for term in company_terms:
      docs = None
      if term in terms_docs:
        docs = terms_docs[term]
      freq.append((term, docs))
    zone.append(freq)
  return zone
