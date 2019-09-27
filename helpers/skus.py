import json

import db.un as db_un

def get_tn(row_num: int):
  skus = db_un.get_en_skus()
  # start index with 1
  sku_str = skus[row_num - 1][1]
  sku_dict = json.loads(sku_str)
  tn = sku_dict['trade_name']
  return tn

def str_to_dict(sku_str: str):
  sku_dict = json.loads(sku_str)
  return sku_dict

def get_dosage(sku_data: dict):
  result = ''
  for item in sku_data['man_forms']:
    result = result + item['dosage_form']['name']
  return result

def get_dosage_form_str(row_num: int):  # таблетки, покрытые плёночной оболочкой
  skus = db_un.get_en_skus()
  sku_str = skus[row_num - 1][1]
  sku_data = str_to_dict(sku_str)
  result = get_dosage(sku_data)
  return result

def get_company(row_num):
  skus = db_un.get_en_skus()
  sku_str = skus[row_num - 1][1]
  sku_data = json.loads(sku_str)
  return sku_data['address']['company']['name']





