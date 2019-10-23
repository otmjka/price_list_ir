### verifed
from db.verified import report_row_num_un_uuid # (0)

### price list
from helpers.prices import load_pulse, show_pline
from helpers.prices import extract_pline

### indexes
from indexes.main import all_idx

### helpers
from helpers.skus import show_sku_by_id


### zones
from zones.common import zone_docs


def get_sources(verifed=False):
  # Verified
  verified = None
  if verifed:
    verified = report_row_num_un_uuid() # (0)
    print('verified loaded')
  # Price list
  plist = load_pulse() # (1)
  print('pulse price loaded')

  #
  # Indexes
  #
  idx = all_idx()
  return verified, plist, idx

# through verified skus
def through_verifed(verified, plist, idx):
  tn_terms_docs = idx['tn_idx']['terms_docs']
  dasage_terms_docs = idx['dosage_idx']['terms_docs']
  company_terms_docs = idx['company_idx']['terms_docs']

  verified_items = list(verified.items())[:10]
  for i, (price_i, un_id) in enumerate(verified_items):
    print('[{}]'.format(price_i))
    # price
    show_pline(i, price_i, plist)
    # verified
    print(show_sku_by_id(un_id, idx))
    pname, pcompany = extract_pline(price_i, plist)

    tn_zone = zone_docs(pname, tn_terms_docs)
    print('\ntn: \n{}'.format(tn_zone))

    dosage_zone = zone_docs(pname, dasage_terms_docs)
    print('\ndosage: \n{}'.format(dosage_zone))

    company_zone = zone_docs(pname, company_terms_docs)
    print('\ncompany: \n{}'.format(company_zone))

###
### Body
###

if __name__ == '__main__':
  verified, plist, idx = get_sources()
  through_verifed(verified, plist, idx)

