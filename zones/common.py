from helpers.skus import show_sku_by_row
from helpers.strings import get_bow


def zone_docs(sku_name, terms_docs):
  name_terms = get_bow(sku_name)
  freq = list()
  for term in name_terms:
    docs = None
    if term in terms_docs:
      docs = terms_docs[term]
    freq.append((term, docs))
  return freq

###
# tn_zone
def flat_zone(zone):
  flat_skus = list()
  for t, docs in zone:
    if docs is None:
      continue
    flat_skus += docs
  return flat_skus

def flat_tn(tn_zone):
  return flat_zone(tn_zone)

def flat_dosage_zone(dosage_zone, skus_by_dosage_row):
  dosage_res = list()
  for term, dosage_docs in dosage_zone:
    if dosage_docs is None:
      dosage_res.append((term, None))
      continue
    term_skus_docs = list()
    for ddoc in dosage_docs:
      if ddoc not in skus_by_dosage_row:
        # print('dosage doc [{}] not present in skus'.format(ddoc))
        continue
      skus_docs = skus_by_dosage_row[ddoc]
      term_skus_docs += skus_docs
    dosage_res.append((term, term_skus_docs))
  flat_skus_dosage = list()
  for ft, ft_docs in dosage_res:
    if ft_docs is None:
      continue
    flat_skus_dosage += ft_docs
  return flat_skus_dosage


def flat_company_zone(c_zone, skus_by_company_row):
  res = list()
  for term, docs in c_zone:
    if docs is None:
      res.append((term, None))
      continue
    term_skus_docs = list()
    for ddoc in docs:
      if ddoc not in skus_by_company_row:
        # print('dosage doc [{}] not present in skus'.format(ddoc))
        continue
      skus_docs = skus_by_company_row[ddoc]
      term_skus_docs += skus_docs
    res.append((term, term_skus_docs))
  flat_skus = list()
  for ft, ft_docs in res:
    if ft_docs is None:
      continue
    flat_skus += ft_docs
  return flat_skus

#
# Weight
#
def add_lists(lists, weights, idx):
  d = dict()
  for i, item_list in enumerate(lists):
    for item in item_list:
      if item not in d:
        d[item] = 0
      d[item] += weights[i]
  result = [(doc, w, show_sku_by_row(doc, idx)) for doc, w in sorted(d.items(), key=lambda t: t[1], reverse=True)]
  return result

# [flat_skus_tn, flat_skus_dosage, flat_skus_c], [0.5, 0.4, 0.1])

def show_res(res, sku_row, idx):
  sel = res[:10]
  for i, (rsku_row, value) in enumerate(sel):
    if sku_row == rsku_row:
      print('---> ', i, rsku_row, value, show_sku_by_row(rsku_row, idx))
    else:
      print(i, rsku_row, value, show_sku_by_row(rsku_row, idx))


def flat_zones(zones, skus_by_dosage_row, skus_by_company_row):
  tn_zone, dosage_zone, company_zone = zones
  flat_skus_tn = flat_tn(tn_zone)
  flat_skus_dosage = flat_dosage_zone(dosage_zone, skus_by_dosage_row)
  flat_skus_company = flat_company_zone(company_zone, skus_by_company_row)
  return flat_skus_tn, flat_skus_dosage, flat_skus_company


def show_flats(flats):
  flat_skus_tn, flat_skus_dosage, flat_skus_company = flats
  print('\nflat_skus_tn: \n{}\n'.format(len(flat_skus_tn)))
  print('\flat_skus_dosage: \n{}\n'.format(len(flat_skus_dosage)))
  print('\flat_skus_company: \n{}\n {}...'.format(len(flat_skus_company), flat_skus_company[:10]))


def handle_zones(pname, pcompany, idx):
  tn_terms_docs = idx['tn_idx']['terms_docs']
  dasage_terms_docs = idx['dosage_idx']['terms_docs']
  company_terms_docs = idx['company_idx']['terms_docs']

  tn_zone = zone_docs(pname, tn_terms_docs)  # trade_name
  dosage_zone = zone_docs(pname, dasage_terms_docs)  # dosage docs
  company_zone = zone_docs(pcompany, company_terms_docs)  # company
  return tn_zone, dosage_zone, company_zone


def show_zones(zones):
  tn_zone, dosage_zone, company_zone = zones
  print('\ntn: \n{}'.format(tn_zone))
  print('\ndosage: \n{}\n'.format(dosage_zone))

  print('\ncompany: {} \n{}'.format(company_zone))