from db.pg import pg_con


def get_companies():
  conn, cursor = pg_con(dbname='cmpny')
  query = 'select c.id, c.original_name, c.name_rus, c.name_rus_short from companies as c order by c.id;'
  cursor.execute(query)
    # 'select r."rowNumber", n."rskuId", n."iskuId" from "NSKUs" as n inner join "RSKUs" as r on n."rskuId"=r.id where n."type" = %s and n."status" = %s',
    # ('medicine', 'verified',))
  recs = cursor.fetchall()

  # verf_row_num_un_uuid = dict([(row_num, un_uuid) for row_num, rsku_id, un_uuid in recs])
  # verf_row_num_un_uuid
  return recs

def get_companies_synonyms():
  conn, cursor = pg_con(dbname='cmpny')
  query = "select cs.company_id, cs.name from company_synonyms as cs order by cs.company_id;"
  cursor.execute(query)
  recs = cursor.fetchall()
  return recs

