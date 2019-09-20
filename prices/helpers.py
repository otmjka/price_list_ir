import pandas as pd

def load_pulse():
  filename = '/Users/admin/projects/pharm-portal/syn-node/user_data/price_lists/rskus_pulse_new.xls'
  price_list = pd.read_excel(filename)
  return price_list

def get_med_items(plist):
  type_col = plist.columns[3]
  types = plist[type_col].unique()
  type_med = types[2]
  result = plist[plist[type_col] == type_med]
  return result

def get_price_item(plist):
  COMPANY_COL = plist.columns[2]
  TN_COL = plist.columns[1]  # trade name column

  name, company = plist[:1][[TN_COL, COMPANY_COL]].values[0]

  return name, company