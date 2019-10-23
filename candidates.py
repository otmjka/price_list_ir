from db.pg import pg_con

# prices

from helpers.prices import load_price_list
from helpers.prices import XLS, CSV
from helpers.prices import cached as pcached

from servers.helpers import get_candidates
from indexes.main import all_idx
from helpers.strings import get_bow

from config.config import SRC_PATH, UPLOADS_LIST

def get_pitem(index: int, plist):
  cols = plist.columns[:3]
  pcode, pname, pcompany = plist[cols].iloc[[index]].values[0]
  return pname, pcompany

def maxmin(candidates):
  skus_to_show = candidates['scored_skus']
  mx = 0 # max
  mn = 0 # min
  for un_id, score, s in skus_to_show:
    mx = max(score, mx)
    mn = max(score, mn)
  return mx, mn

def show_maxmin(candidates):
  mx, mn = maxmin(candidates)
  print('max: {} min: {}'.format(mx, mn))

def load_price_lists(amount=1):
  ### load price lists
  uploads = UPLOADS_LIST # [:amount]

  for upload_id, fn, ext, sel_columns in uploads:
    pl = '{}/{}'.format(SRC_PATH,
                        fn)  # cur_pl = UPLOADS_LIST[0] # ('59e96010-b2cc-11e9-9340-d9e56c905807', 'rskus_pulse_new.xls', 'xls')
    load_price_list(pl, cache_name=fn, ext=ext)

def candidates_by_index(index, plist, idx, debug=False):
  pitem = get_pitem(index, plist)
  pname, pcompany = pitem

  if debug:
    print('{}\n{}'.format(pname, get_bow(pname)))

  candidates = get_candidates(pname, pcompany, idx)
  return candidates


def handle_candidate(cur_index: int, plist, idx, debug=False):
  candidates = candidates_by_index(cur_index, plist, idx)
  weight_filtered_skus = candidates['weight_filtered_skus']

  if debug:
    show_maxmin(candidates)

    scored_skus_count = len(candidates['scored_skus'])
    weight_filtered_skus_count = len(weight_filtered_skus)
    print('[{}] all candidates: {}\nweight 0.3 filtered {}'.format(cur_index, scored_skus_count,
                                                                   weight_filtered_skus_count))
  return weight_filtered_skus  ### ! ###


def get_all(plist, idx, debug):
  candidates_list = []
  for cur_index in range(len(plist)):
    pitem = get_pitem(cur_index, plist)
    candidates_list.append((pitem, handle_candidate(cur_index, plist, idx, debug)))

  return candidates_list

def rskus_row_id():
  conn, cursor = pg_con()
  result = {}
  query = 'select r."rowNumber" as rn, r.id, r."uploadId" as u_id from "RSKUs" as r order by u_id, rn;'

  cursor.execute(query)
  recs = cursor.fetchall()
  conn.close()
  # 1 rsku_id u_id
  for row_num, rsku_id, upload_id in recs:
    if upload_id not in result:
      result[upload_id] = {}
    result[upload_id][row_num] = rsku_id
  return result


def save_candidates_batch(items, idx):
  conn, cursor = pg_con()
  iskus_idx = idx['iskus_idx']
  items_filtered = []
  for w, rid, un_id in items:
    if un_id not in iskus_idx:
      print('not un_jd in iskus table: [{}]'.format(un_id))
      q = 'INSERT INTO "ISKUs" VALUES {};'
      values = [
        '(\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',{}, {})'.format(un_id, "\'\'", "\'\'", "\'\'", "\'\'", 'now()', 'now()')]
      values_str = ','.join(values)
      query = q.format(values_str)
      cursor.execute(query)
      conn.commit()
      idx['iskus_idx'].add(un_id)
    items_filtered.append((w, rid, un_id))
  q = 'INSERT INTO "Candidates" ({}) VALUES {};'
  columns = ['"degreeOfSimilarity"', '"rskuId"', '"iskuId"', '"createdAt"', '"updatedAt"']
  columns_str = ','.join(columns)
  values = ["({}, '{}', '{}', now(), now())".format(w, rid, un_id) for w, rid, un_id in items_filtered]
  values_str = ',\n'.join(values)
  query = q.format(columns_str, values_str)

  cursor.execute(query)
  conn.commit()
  conn.close()
  print(query)

def make_rsku_idx():
  rskus_row_id_idx = rskus_row_id()
  return rskus_row_id_idx

# 33909 => 68
def get_bunch_count(l, bunch_size=500):
  num = l / bunch_size
  num = int(num) + 1 if num > int(num) else int(num)
  return num

def get_next_range(bunches_amount, total_len, bunch_size=500):
  for bunch_i in range(bunches_amount):
    left = bunch_i * bunch_size  # 0
    right = ((bunch_i + 1) * bunch_size)  # 499
    if right > total_len:
      right = total_len
    yield left, right

def get_candidates_to_save(sel_values, idx, limit=100):
  candidates_list = []
  for i, (cur_value) in enumerate(sel_values):
    if i % 50 == 0:
      print(i)
    pname, pcompany = cur_value
    candidates = get_candidates(pname, pcompany, idx)
    weight_filtered_sku_candidates = candidates['weight_filtered_skus']
    if type(limit) == int:
      weight_filtered_sku_candidates = weight_filtered_sku_candidates[:limit]
    candidates_list.append(((pname, pcompany), weight_filtered_sku_candidates))
  return candidates_list

# def make_data_to_save(candidates, idx):
#   rskus_row_id_idx = idx['rskus_row_id_idx']
#   rsku_start_index = 1
#   to_save = []
#   for i, (plist_label, pcand) in enumerate(candidates):
#     rsku_row = i + rsku_start_index
#     rsku_id = rskus_row_id_idx[rsku_row]
#     print(i, rsku_row)
#     print(plist_label, len(pcand))
#     print('\n-------- [{}]'.format(rsku_id))
#     for cand_i, (sku_row, w, _debug_str) in enumerate(pcand[:3]):
#       un_id = idx['skus_idx']['rows_id'][sku_row]
#       print('{} | {} {} [{}][{}]'.format(cand_i, w, _debug_str, sku_row, un_id))
#       print('w:[{}] r:[{}] un:[{}]'.format(w, rsku_id, un_id))
#       to_save.append((w, rsku_id, un_id))
#     print('\n--------'.format())
#   return to_save
def make_data_to_save(candidates, upload_id, idx, left=0):
  rskus_row_id_idx = idx['rskus_row_id_idx'][upload_id]
  rsku_start_index = 1
  to_save = []
  for i, (plist_label, pcand) in enumerate(candidates):
    rsku_row = i + rsku_start_index + left
    rsku_id = rskus_row_id_idx[rsku_row]
    for cand_i, (sku_row, w, _debug_str) in enumerate(pcand[:40]):
      un_id = idx['skus_idx']['rows_id'][sku_row]
      to_save.append((w, rsku_id, un_id))
  return to_save

def make_iskus_idx():
  conn, cursor = pg_con()
  q = 'select i.id from "ISKUs" as i'
  cursor.execute(q)
  recs = cursor.fetchall()
  return set([rec[0] for rec in recs])

def start():
  idx = all_idx()
  rskus_row_id_idx = make_rsku_idx()
  iskus_idx = make_iskus_idx()

  idx['rskus_row_id_idx'] = rskus_row_id_idx
  idx['iskus_idx'] = iskus_idx
  load_price_lists()
  for upload_id, price_fn, _ext, target_columns in UPLOADS_LIST:
    print('{} {} {}'.format(upload_id, price_fn, target_columns))
    plist = pcached[price_fn]

    #
    # through the plist
    #
    lenp = len(plist)
    bunches_amount = get_bunch_count(lenp)

    for left, right in get_next_range(bunches_amount, lenp):
      print('{} {}'.format(left, right))
      sel_cols = plist.columns[target_columns]
      selected = plist[sel_cols][left:right]
      sel_values = selected.values
      bunch_candidates = get_candidates_to_save(sel_values, idx)
      to_save = make_data_to_save(bunch_candidates, upload_id, idx, left=left)
      save_candidates_batch(to_save, idx)

if __name__ == '__main__':
  start()


