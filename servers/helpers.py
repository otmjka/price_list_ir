from helpers.skus import show_sku_by_row, get_sku_id_by_row
from helpers.skus import get_sku_data_by_row, get_tn_from_data

from indexes.company import get_company_sname

from zones.common import zone_docs, add_lists
from zones.tn import tn_zone

def get_pitem(index: int, src):
  plist = src[1]
  cols = plist.columns[:3]
  pcode, pname, pcompany = plist[cols].iloc[[index]].values[0]
  return dict(pcode=pcode, pname=pname, pcompany=pcompany, index=index)

def handle_tn_zone(pname, idx):
  tn = list()
  tn_zone_skus = tn_zone(pname, idx['tn_idx']['terms_docs'])
  # { `term`: [sku_doc_0, ...], ...}
  # TODO:
  # go through sku_docs and get all trade_names
  # 1. one-word-trade-name
  # 2. two-3-4-5-n-word-trade-name
  # учитывать позицию
  for i, (term, sku_docs) in enumerate(tn_zone_skus):
    if sku_docs == None:
      sku_term_info = dict(index=i, term=term, sku_docs=[], sku_un_id_list=[], sku_trade_names=[])
      tn.append(sku_term_info)
      continue
    sku_un_id_list = [get_sku_id_by_row(sku_doc, idx) for sku_doc in sku_docs]
    sku_trade_names = [get_tn_from_data(get_sku_data_by_row(sku_doc, idx)) for sku_doc in sku_docs]
    sku_term_info = dict(index=i, term=term, sku_docs=sku_docs, sku_un_id_list=sku_un_id_list,
                         sku_trade_names=sku_trade_names)
    tn.append(sku_term_info)
  # TODO: надо смотреть сколько в трейд-нейме слов
  #
  return tn

def handle_company_zone(pcompany, idx, debug=False):
  skus_by_company_row = idx['skus_by_company_row']

  company_terms_docs = idx['company_idx']['terms_docs']
  company_terms_docs = zone_docs(pcompany, company_terms_docs)
  company_terms_sname = list() # {`щелковский`: [имя1, ...]}
  term_skus_docs = list()
  for i, (term, term_company_docs) in enumerate(company_terms_docs):
    if term_company_docs == None:
        continue
    short_names = [get_company_sname(cdoc, idx) for cdoc in term_company_docs]
    for cdoc in term_company_docs:
      if cdoc not in skus_by_company_row:
        if debug:
          print('company doc {} not in idx'.format(cdoc))
        continue
      skus_docs = skus_by_company_row[cdoc]
      term_skus_docs += skus_docs
    company_terms_sname.append((term, short_names))
  return dict(terms_docs=company_terms_docs, company_terms_sname=company_terms_sname, term_skus_docs=term_skus_docs)

def get_candidates(pname, pcompany, idx, weight_filter=0.3):
  res = dict()
  # tn zone
  tn = handle_tn_zone(pname, idx)
  res['tn'] = tn
  # company zone
  res['company'] = handle_company_zone(pcompany, idx)

  flat = list()
  for term in tn:
    flat += term['sku_docs']
  res['flat'] = flat
  res['flat_sku_value'] = [show_sku_by_row(doc, idx) for doc in res['flat']]

  tn_skus = res['flat']
  company_skus = res['company']['term_skus_docs']
  scored_skus = add_lists([tn_skus, company_skus], [0.5, 0.3], idx)
  weight_filtered_skus = [sku for sku in scored_skus if sku[1] > weight_filter]
  res['scored_skus'] = scored_skus
  res['weight_filtered_skus'] = weight_filtered_skus
  return res

def candidates_by_price_row(i, src: dict):
  idx = src[2]
  pitem_dict = get_pitem(i, src) # price item by row number

  pname = pitem_dict['pname']
  pcompany = pitem_dict['pcompany']

  candidates_result = get_candidates(pname, pcompany, idx)

  result = {**pitem_dict, **candidates_result}

  return result

def search_tn(query, idx):
  terms_docs = idx['tn_idx']['terms_docs']
  response = {'terms': dict(), 'tn_list': list(),
              'part_tn_list': list()}
  if query in terms_docs:
    docs = terms_docs[query]
    if query not in response['terms']:
      response['terms'][query] = dict()
      response['terms'][query]['docs'] = docs
      response['terms'][query]['skus'] = list()
      for doc in docs:
        response['terms'][query]['skus'].append(show_sku_by_row(doc, idx))
    if len(docs) > 0:
      tn = get_tn_from_data(get_sku_data_by_row(docs[0], idx))
      if tn not in response['tn_list']:
        response['tn_list'].append(tn)

  for key in terms_docs.keys():
    if query not in key:
      continue
    response['part_tn_list'].append(key)
  return response