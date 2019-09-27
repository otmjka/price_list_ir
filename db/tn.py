from logging import info

from db.common import TN_TERM_DOCS
from db.common import conn, cursor, cache
from db.common import truncate_table

#
# `trade_name`
#

def get_term_docs_table(cursor=cursor):
  q = 'select term, docs_json from {} order by term'
  query = q.format(TN_TERM_DOCS)
  cursor.execute(query)
  records = cursor.fetchall()
  info('loaded records: {}'.format(len(records)))
  return records

# TODO: save prefix, rw is option
def save_term_docs_table(items, conn=conn, cursor=cursor, rw=True):
  tn = TN_TERM_DOCS
  truncate_table(table_name=tn, rw=rw)

  values = ['(\'{}\',\'{}\')'.format(term, docs_json) for term, docs_json in items]
  values = ','.join(values)

  q = 'INSERT INTO {} VALUES {};'
  query = q.format(tn, values)
  cursor.execute(query)
  conn.commit()
