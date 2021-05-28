# Reads Hops from database and attempts to locate the geocordinates of them
# then enters the lat, lon and address back into the geo table  

import mysql.connector
import json
from geopy.geocoders import Nominatim
from html_create_tr import Html_Create 
from geopy.distance import geodesic

# A Python library to gather IP address details (ASN, prefix, resource holder, reverse DNS) using the RIPEStat API,
# with a basic cache to avoid flood of requests and to enhance performances. https://pypi.org/project/ipdetailscache/

from pierky.ipdetailscache import IPDetailsCache
cache = IPDetailsCache(IP_ADDRESSES_CACHE_FILE = "cache/ip_addr.cache", IP_PREFIXES_CACHE_FILE = "cache/ip_pref.cache", MAX_CACHE = 604800, Debug = False )

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="brindle7",
    database="ipgeo"
    )
cursor = mydb.cursor()
geolocator = Nominatim(user_agent="aswindow")



'''
sql = "select * from asn_address"
cursor.execute(sql)
addresses = cursor.fetchall()
'''

sql = "select * from hops"
cursor.execute(sql)
hops = cursor.fetchall()

previous_id = 0
for hop in hops:
    print (hop)

    
    asn = hop[8]
    hop_id = hop[0]
    print(asn)
    sql = "select * from asn_address where asn = %s"
    val = (asn,)
    cursor.execute(sql,val)
    asn_address = cursor.fetchone()
    print (asn_address)
    
    ip = asn_address[7]
    
    if asn_address == None:
        ''' if ip.startswith("10") or 
                ip.startswith('17.16','17.17','17.18','17.19','17.20'
                            '17.21','17.22','17.23','17.24','17.25'
                            '17.26','17.27','17.28','17.29','17.30'
                            '17.31') or
                ip.startswith("192.168"):
        '''

        
    address_id = asn_address[0]
    previous_id = address_id
    sql = "UPDATE hops SET address_id = %s WHERE id = %s"
    val = (address_id, hop_id)
    #cursor.execute(sql,val)
    #mydb.commit() 
    print(val)






    #holder = address[2]
    #addr = address[3]


'''   
    target_probe = measurements[measurement]
    sql = "select * from hops where measurement= %s"
    val = (measurement,)
    cursor.execute(sql,val)
    ids = cursor.fetchall()
    #print(ids)
    #probe = hops[3]
    m_dict[measurement] = {}
    for id in ids:
        
        probe = id[2]
        hop = id[3]
        print (probe,hop)
        if probe not in m_dict[measurement]:
            m_dict[measurement][probe] = {}
        m_dict[measurement][probe][hop] = {}
        m_dict[measurement][probe][hop]['rtt'] = id[4]
        m_dict[measurement][probe][hop]['hostname'] = id[5]
        m_dict[measurement][probe][hop]['prefix'] = id[6]
        m_dict[measurement][probe][hop]['ip'] = id[7]
        m_dict[measurement][probe][hop]['asn'] = id[8]
        sql = "select * from asn_address where asn = %s"
        val = (id[8],)
        cursor.execute(sql,val)
        asn_a = cursor.fetchall()

        if asn_a == []:
            continue
        print(asn_a[0])
        m_dict[measurement][probe][hop]['holder'] = asn_a[0][2]

        # Now geolocate the hop
        x,y,address = check_location(id[8],ids[2],id[5]) # asn, holder, hostname

        print(x,y,address)
'''



    

      


    
    #hops_dict = Convert(hops)
    #print (hops_dict)