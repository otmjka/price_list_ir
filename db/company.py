from db.pg import pg_con


def get_companies():
  conn, cursor = pg_con(dbname='cmpny')
  query = 'select c.id, c.original_name, c.name_rus, c.name_rus_short from companies as c order by c.id;'
  cursor.execute(query)
    # 'select r."rowNumber", n."rskuId", n."iskuId" from "NSKUs" as n inner join "RSKUs" as r on n."rskuId"=r.id where n."type" = %s and n."status" = %s',
    # ('medicine', 'verified',))
  recs = cursor.fetchall()
  conn.close()
  # verf_row_num_un_uuid = dict([(row_num, un_uuid) for row_num, rsku_id, un_uuid in recs])
  # verf_row_num_un_uuid
  return recs

def get_companies_synonyms():
  conn, cursor = pg_con(dbname='cmpny')
  query = 'select cs.company_id, cs.name from company_synonyms as cs order by cs.company_id;'
  cursor.execute(query)
  recs = cursor.fetchall()
  conn.close()
  return recs

def get_addr_company_table():
  conn, cursor = pg_con(dbname='cmpny')
  q = 'select a.id, a.company_id from addresses as a order by a.id;'
  cursor.execute(q)
  recs = cursor.fetchall()
  conn.close()
  conn = None
  cursor = None

  cmpy = dict()
  addr = [(addr_id, c_id) for addr_id, c_id in recs]
  for addr_id, c_id in recs:
    docs = c_id in cmpy and cmpy[c_id] or list()
    docs.append(addr_id)
    cmpy[c_id] = docs

  return dict(recs=recs,
              addr_cmp=dict(addr),
              cmp_addreses=cmpy)

