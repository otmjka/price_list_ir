import pandas as pd

cached = dict()
XLS = 'xls'
CSV = 'csv'

def load_price_list(plpath, cache_name=None, ext=XLS):
  if ext == XLS:
    price_list = pd.read_excel(plpath)
  if ext == CSV:
    price_list = pd.read_csv(plpath, sep='\t')

  if cache_name != None:
    cached[cache_name] = price_list

  return price_list

def load_pulse():
  if 'plist_cached' in cached:
    return cached['plist_cached']
  filename = '/Users/admin/projects/pharm-portal/syn-node/user_data/price_lists/rskus_pulse_new.xls'
  price_list = pd.read_excel(filename)
  cached['plist_cached'] = price_list
  return price_list

def plist_index(plist):
  if 'plist_index' in cached['plist_index']:
    return cached['plist_index']
  cached['plist_index'] = dict([(code, i) for i, code in enumerate(plist[plist.columns[0]].values)])
  return cached['plist_index']

def by_code(code, code_dict, plist):
  i = code_dict[code]
  return plist[i:i + 1]

# 'ЖНВЛП'
def get_live_important_items(plist):
  type_col = plist.columns[3]
  types = plist[type_col].unique()
  type_live_imp = types[3] # 'ЖНВЛП'
  live_imp_df = plist[plist[type_col] == type_live_imp]
  result = list(live_imp_df[live_imp_df.columns[0:3]].values)
  return result

def get_pulse_live_imp():
  plist = load_pulse()
  live_imp = get_live_important_items(plist)
  return live_imp

def extract_pline(price_i, plist):
  # price
  sel_plist = plist[price_i - 1:price_i]
  sel_cols = sel_plist[sel_plist.columns[:3]]
  values = sel_cols.values[0]
  code, name, company = values
  return name, company

def show_pline(i, price_i, plist):
  name, company = extract_pline(price_i, plist)
  print('{}. [{}]\nP: {} [{}]'.format(i, price_i, name, company))