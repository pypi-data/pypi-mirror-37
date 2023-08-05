import phoenixdb
import phoenixdb.cursor

def qtx_phoenix_con(host, port, commit=True):
    db_url = 'http://'+str(host)+':'+str(port)+'/'
    conn = phoenixdb.connect(db_url, autocommit=commit)
    return conn.cursor()

def qtx_mssql_con():
    pass

def qtx_mysql_con():
    pass
