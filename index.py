import services.log
from logging import info
from indexes.tn import build_indexes

from prices.helpers import get_pulse_live_imp

info('start')

# 1. build indexes
indexes = build_indexes()
rows_id = indexes['rows_id']
terms_docs = indexes['terms_docs']

# 2. get med items from price_list
live_imp = get_pulse_live_imp()

# 3. trade_name zone
# 4. company zone
# 5. dosage_form zone # таблетки, покрытые плёночной оболочкой
# 6. active chemical element
## inn # # ситаглиптин sitagliptin sitagliptinum 0.05 грамм гметформин metformin metforminum 1 грамм г
## measure_unit
# 7. count zone # x28(28 шт)

# => large list of docs(un_id)

# 8. for each row in price list:
# to all docs was found in zone_i assign zone_i_weight
## zones = [tn, company, dosage, active_elem, count]
## weights = [zone_i_weight] i in [0, len(zones) - 1]
## sum([weight in weights]) = 1

# 9. after sum weights for certain doc
# price row item => [(doc, score), ...]
# score value in [0, 1]
# 10. sort by score

# check with verified version




