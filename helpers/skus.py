import json

import db.un as db_un
from enums.common import TRADE_NAME

def get_tn(row_num: int):
  skus = db_un.get_en_skus()
  # start index with 1
  sku_str = skus[row_num - 1][1]
  sku_dict = json.loads(sku_str)
  tn = sku_dict[TRADE_NAME]
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

def get_tn_from_data(sku_data):
  return sku_data[TRADE_NAME]

def get_lek_form(sku_data):
  return sku_data[TRADE_NAME]

def show_sku(sku_data: dict):
  # sku_row = skus_id_rows_idx[un_id]
  # un_sku_data = un_skus[row]
  tn = get_tn_from_data(sku_data)
  lform = get_lek_form(sku_data)
  # skus = db_un.get_en_skus()







