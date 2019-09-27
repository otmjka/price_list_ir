import psycopg2 as pg

def pg_con(dbname='syn', user='syn_rw',
                    host='localhost', password='example'):
  conn = pg.connect(dbname=dbname, user=user,
                    host=host, password=password)
  cursor = conn.cursor()
  return conn, cursor
