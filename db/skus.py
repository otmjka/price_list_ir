from db.pg import pg_con

def un_db_conn():
  conn, cursor = pg_con(dbname='un')
  return conn, cursor

