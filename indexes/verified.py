from helpers.skus import get_sku_data_by_row
from helpers.skus import get_tn_from_data
from indexes.forms import get_dosage_names, get_dosage_rows
from indexes.company import company_short_name
from indexes.company import get_company_row_by_sku_data

def get_un_id_by_verifed(price_row, verified):
  un_id = verified[price_row]
  return un_id

def get_sku_row_by_verifed(price_row, verified, idx):
  skus_id_rows_idx = idx['skus_idx']['rows_id_inv']
  un_id = verified[price_row]
  return skus_id_rows_idx[un_id]

def sku_data_by_price_row(price_row, verified, idx):
  skus_id_rows_idx = idx['skus_idx']['rows_id_inv']

  un_id = verified[price_row]
  sku_row = skus_id_rows_idx[un_id]
  sku_data = get_sku_data_by_row(sku_row, idx)
  return sku_data


def show_verified_tn(tn, sku_row, in_results):
  print('[{}] [{}] => {}'.format(tn, sku_row, in_results))


def show_verified_dosage(dosage_names, dosage_rows, in_results):
  print('[{}] [{}] => {}'.format(dosage_names, dosage_rows, in_results))


def show_verified_company(company, company_row, in_results):
  print('[{}] [{}] => {}'.format(company, company_row, in_results))


def show_verified(price_row: int, verified, zones, idx):
  flat_skus_tn, flat_skus_dosage, flat_skus_company = zones
  sku_row = get_sku_row_by_verifed(price_row, verified, idx)
  sku_data = sku_data_by_price_row(price_row, verified, idx)
  # common
  un_id = get_un_id_by_verifed(price_row, verified)
  print('[{}]'.format(un_id))
  # trade_name
  tn = get_tn_from_data(sku_data)
  in_results = sku_row in flat_skus_tn
  show_verified_tn(tn, sku_row, in_results)
  # Dosage
  dosage_names = get_dosage_names(sku_data, idx)
  dosage_rows = get_dosage_rows(sku_data, idx)
  in_results = sku_row in flat_skus_dosage
  show_verified_dosage(dosage_names, dosage_rows, in_results)
  # Company
  company_row = get_company_row_by_sku_data(sku_data, idx)
  company = company_short_name(sku_data, idx)
  in_results = sku_row in flat_skus_company
  show_verified_company(company, company_row, in_results)

def get_sku_index_in_results(sku_row, results, none_index=-20):
  for i, (rsku_row, value) in enumerate(results):
    if rsku_row == sku_row:
      return i
  return none_index
