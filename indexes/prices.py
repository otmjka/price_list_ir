from utils.filehash import filehash
from db.uploads import create_uploads_table, save_to_uploads

from config.config import SRC_PATH, UPLOADS_LIST

def fullfill_uploads_table():
  create_uploads_table()
  items_to_save = []

  for _, fn, ext, cols in UPLOADS_LIST:
    fp = '{}/{}'.format(SRC_PATH, fn)
    fp_hash = filehash(fp) # md5, sha1
    items_to_save.append((fp, fp_hash))

  return save_to_uploads(items_to_save)
