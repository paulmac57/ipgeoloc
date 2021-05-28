import os
import sqlite3

# Default database in same folder as this script
DEFAULT_DB_PATH = os.path.join(os.path.dirname(__file__), 'peeringdb.sqlite3')

# Connection to Peeringdb locally Synced database
def db_connect(db_path=DEFAULT_DB_PATH):
    con = sqlite3.connect(db_path)
    return con

print( DEFAULT_DB_PATH)

peeringdb_con = db_connect()
peeringdb_cur = peeringdb_con.cursor()
ipaddress = '196.60.9.24'
ipaddress = '196.223.14.99'
#fac_id = '2172'
sql = 'select net_id from peeringdb_network_ixlan where ipaddr4 = ?'
#sql = 'select * from peeringdb_facility where id = ?'
#val = (str(fac_id),)
#print(fac_id)
val = (str(ipaddress),)
peeringdb_cur.execute(sql,val)
print(ipaddress)
fac_id = peeringdb_cur.fetchone()[0]

sql = 'select fac_id from peeringdb_network_facility where net_id = ?'
val = (str(fac_id),)
peeringdb_cur.execute(sql,val)
info = peeringdb_cur.fetchone()[0]
print(info)

sql = 'select * from peeringdb_facility where id = ?'
val = (str(info),)
print(fac_id)
peeringdb_cur.execute(sql,val)

info = peeringdb_cur.fetchall()
print(info)
