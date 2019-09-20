from db.common import get_en_skus, save_idx_row_id
from db.common import save_tn_dict, load_tn_term_dict
from indexes.tn import build_indexes, build_index_row_en_uuid, build_tn_dict, get_terms_skus
from indexes.tn import intersection

from prices.helpers import load_pulse, get_med_items, get_price_item
from helpers.strings import tokenize
from helpers.reports import result_report

print('start')

loglog('check module imports')

# get ISKUS
idx_source = get_en_skus()

# 1. build index row_num/en_uuid
idx_row_id = build_indexes(idx_source)
# save_idx_row_id(idx_row_id)

# 2. build index term/docs list
tn_term_dict = build_tn_dict(idx_source)
save_tn_dict(tn_term_dict)

# 3. load (2.)
tn_term_dict_loaded = load_tn_term_dict()

# 4. get med items from price_list
plist = load_pulse()
med_list = get_med_items(plist)

#5. get an item from med_list
name, company = get_price_item(med_list) # name_col, company_col
print('\n\nname:', name)
print('company:', company)
print('\n')
name_terms = tokenize(name) # name
# company_terms = tokenize(item.company)

# return
# [('A_term', [term_sku_0, ..., term_sku_n]), ...]
terms_skus = get_terms_skus(name_terms, tn_term_dict_loaded)

# 0, few, normal, many
# simple, all not empty, and len(term) > 2
result = intersection(terms_skus)

result_report(result)





