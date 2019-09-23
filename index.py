import services.log
from logging import info, debug
from db.common import get_en_skus
from indexes.tn import build_indexes, get_terms_skus
from indexes.tn import intersection

from prices.helpers import load_pulse, get_med_items, get_price_item
from helpers.strings import tokenize
from helpers.reports import result_report

info('start')
# get ISKUS
idx_source = get_en_skus()

# 1. build index row_num/en_uuid
row_id, token_docs, token_tn, token_keys = build_indexes(idx_source)

# 4. get med items from price_list
plist = load_pulse()
med_list = get_med_items(plist)

#5. get an item from med_list
name, company = get_price_item(med_list) # name_col, company_col

debug('\n\nname: {}'.format(name))
debug('company: {}'.format(company))
debug('\n')

name_terms = tokenize(name) # name
# company_terms = tokenize(item.company)

# return
# [('A_term', [term_sku_0, ..., term_sku_n]), ...]
terms_skus = get_terms_skus(name_terms, token_docs)

# 0, few, normal, many
# simple, all not empty, and len(term) > 2
result = intersection(terms_skus)

result_report(result)





