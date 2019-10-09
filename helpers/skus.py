import json

import db.un as db_un

# show_sku_by_id
from indexes.forms import get_dosage_names, get_dosage_rows
from indexes.company import company_short_name
from indexes.skus import get_sku_data

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

def show_sku_data(sku_data, idx, un_row=0, un_id=''):
  # trade_name
  tn = get_tn_from_data(sku_data)
  # Dosage
  dosage_names = get_dosage_names(sku_data, idx)
  dosage_rows = get_dosage_rows(sku_data, idx)
  # Company
  company = company_short_name(sku_data, idx)
  return '[{}] [{}] [{}] [{}] [{}]'.format(tn, ';'.join(dosage_names), company, un_row, un_id)

def get_sku_data_by_row(row_num: int, idx: dict):
  un_skus = idx['un_skus']
  un_sku_data = un_skus[row_num]
  _sku_id, sku_data = un_sku_data
  return sku_data

def show_sku_by_id(un_id, idx):
  row_num, sku_data = get_sku_data(un_id, idx)
  return show_sku_data(sku_data, idx, row_num, un_id)

def show_sku_by_row(row_num: int, idx):
  sku_data = get_sku_data_by_row(row_num, idx)
  return show_sku_data(sku_data, idx, un_row=row_num)


