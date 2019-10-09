from db.pg import pg_con
from collections import OrderedDict

def report_row_num_un_uuid():
  # syn DB
  conn, cursor = pg_con()
  cursor.execute("""
    select r."rowNumber", n."rskuId", n."iskuId"
    from "NSKUs" as n
    inner join "RSKUs" as r on n."rskuId"=r.id
    where n."type" = %s and n."status" = %s order by r."rowNumber";""",
    ('medicine', 'verified',))
  recs = cursor.fetchall()

  verf_row_num_un_uuid = OrderedDict([(row_num, un_uuid) for row_num, rsku_id, un_uuid in recs])
  return verf_row_num_un_uuid

#
# select c."degreeOfSimilarity", c."rskuId", c."iskuId"
# from "Candidates" as c
# inner join
# "RSKUs" as r on с."rskuId"=r."rskuId"
# order by c."rskuId", c."degreeOfSimilarity"

def get_candidates():
  q = """
select r."rowNumber", c."degreeOfSimilarity", c."iskuId"
from "Candidates" as c
inner join "RSKUs" as r on c."rskuId" = r.id
order by c."rskuId", c."degreeOfSimilarity" DESC;"""
  conn, cursor = pg_con()
  cursor.execute(q)
  recs = cursor.fetchall()
  conn.close()
  return recs
