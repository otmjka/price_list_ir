import psycopg2 as pg

def pg_con(dbname='syn', user='syn_rw', port='5432',
                    host='localhost', password='example'):
  conn = pg.connect(dbname=dbname, user=user,
                    host=host, password=password, port=port)
  cursor = conn.cursor()
  return conn, cursor

# truncate syn."Candidates"
def truncate_candidates(conn, cursor):
  q = 'truncate "Candidates";'
  cursor.execute(q)
  return conn.commit()

