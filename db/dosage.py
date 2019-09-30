from db.pg import pg_con
from enums.common import DB_DIR


def fetch_dosage_forms():
    conn, cursor = pg_con(dbname=DB_DIR)
    q = 'select d.id, d.name, d.code from dosage_forms as d order by d.id;'
    cursor.execute(q)
    recs = cursor.fetchall()
    conn.close()
    return recs

"""
select d.name from dosage_forms as d where id='aef3b0ca-d3ef-4d32-a078-923f8c6426ce';
select d.id, d.name, d.code from dosage_forms as d order by d.id;
"""

