# ENSURE THAT ENV VARIABLE IS SET EXPORT GOOGLE_API_KEY='<google geocoding API key'

# app to re-create all database tables (set create_table to true)
#except ixps and ixp_ips
# Also read in all data from file "dictionary1.json" created by create_measurements.py
# and loads this data into database (set read_file flag to true)
# IF wish to recreate the (blank) database set the following flag to true
create_table = False
# If wish to read in all data and populate database set the following flag to true
read_file  = True

import json
import os
import re

# ensure to create environment variable in os GOOGLE_API_KEY' = 'google api key' and export it
k = os.environ.get('GOOGLE_API_KEY')
k = 'AIzaSyD19RPrdUrUp0Vlei08vSCpcUBR3FQoxqY'


import mysql.connector
# use free Nominatum to dicover hop coordiantes from address
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="aswindow")
# USing chargeable Google if nominatum fails to find hop coordiantes https://pypi.org/project/geocoder/
import geocoder

from html_create_tr import Html_Create 
from geopy.distance import geodesic
from ipwhois import IPWhois
from pprint import pprint





def get_location(ip):
    # TODO What do we do with 100.64.0.0 to 100.127.255,255 subnet
    # which is recommended according to rfc6598 for use as an address pool
    # for CGN (Carrier-Grade NAT)
    this_add = ''
    # if ip is a private subnet then set address to "local"
    if ip == None:
        this_add = "None"
        x = 0
        y = 0
    elif ip.startswith(('10.','172.16.','172.17.','172.18.','172.19.','172.20.','172.21.','172.22.',
    '172.23.','172.24.','172.25.','172.26.','172.27.','172.28.','172.29.','172.30.','172.31.','192.168.')):
        this_add = "local"
        x = 0
        y = 0
    elif ip.startswith(('100.64.','100.65.','100.66.','100.67.','100.68.','100.69.',
    '100.70.','100.71.','100.72.','100.73.','100.74.','100.75.','100.76.','100.77.','100.78.',
    '100.79.','100.80.','100.81.','100.82.','100.83.','100.84.','100.85.','100.86.','100.87.',
    '100.88.','100.89.','100.90.','100.91.','100.92.','100.93.','100.94.','100.95.','100.96.',
    '100.97.','100.98.','100.99.','100.100.','100.101.','100.102.','100.103.','100.104.','100.105.',
    '100.106.','100.107.','100.108.','100.109.','100.110.','100.111.','100.112.','100.113.','100.114.',
    '100.115.','100.116.','100.117.','100.118.','100.119.','100.120.','100.121.','100.122.','100.123.',
    '100.124.','100.125.','100.126.','100.127.')):
        this_add = "CGN"
        x = 0
        y = 0
    else:
        obj = IPWhois(ip)
        results = obj.lookup_rdap(depth=1)
         
        r = results['objects'].keys()
        # TODO above may return multiple addresses so create a
        # Sense check vs Speed of light
        # to decide which one is best
        # for now just use first address
        
        region = list(r)
        print (region)
        coord_flag = False
        for a in region:
            print (a)
            print(results['objects'][a]['contact']['address'])
            if results['objects'][a]['contact']['address'] != None:
                add = results['objects'][a]['contact']['address']
                
                addresses = list(add)
                
                for b in range(len(addresses)):
                    # print( results['objects'][a]['contact']['address'][b]['value'])
                    this_add = results['objects'][a]['contact']['address'][b]['value']
                    this_add = re.sub('\n', ' ',this_add.rstrip())
                    #print("address is",this_add)
                    if this_add != "None":
                        location = geolocator.geocode(this_add)
                        #print("location is ",location)
                        if location == None :
                            
                            g = geocoder.google(this_add, key = k)
                            if g != None:
                                x = g.lng
                                y = g.lat
                                #print (x,y, " got from GOOGLE")
                                coord_flag = True
                                break
                            
                        else:
                            x = location.longitude
                            y = location.latitude
                            #print (x,y, " got from nominatum")
                            coord_flag = True
                            break
                    
            if coord_flag == True:
                coord_flag == False
                break
    return this_add,x,y

# Use the free Nominatum geocoder unless it cant find the coords of the address then use Google
def get_coords(address):
    company_address = address
    print(company_address)
    location = geolocator.geocode(address)
    if location == None :
        g = geocoder.google(address, key = k)
        x = g.lng
        y = g.lat
    else:
        x = location.longitude
        y = location.latitude

    return x,y




'''
#def check_location(asn,holder,hostname):
    # If an ASN is provided get corordinates from known LOCAL address of that ASN
    target_address = ""   # sample target address 90 Oxford Street, Randburg
    location = geolocator.geocode(target_address)
    hop_address = ''
    # check ASNs to provide address locations
    if asn != 'not announced':
        if asn == '327849':
            hop_address = "189 Olympic Duel Ave,  Randburg"                                 # hop address for ROCKETNET
            location = geolocator.geocode(hop_address)
        if asn == '327750':
            hop_address = "90 Oxford St, Randburg"                                          # hop address for Jenny Internet
            location = geolocator.geocode(hop_address)

        if asn == '36692':
            hop_address = "15 Georgian Cres W, Sandton"                                     # hop address for Cisco Systems Johannesburg
            location = geolocator.geocode(hop_address)
        if asn == '15022':
            hop_address = "16 Elektron Rd, Techno Park, Stellenbosch, 7600, South Africa"                                     # hop address for ADEPT
            location = geolocator.geocode(hop_address)
        if asn == '37670':  
            hop_address = "Smart tech centre, 1 Townsend St, Townsend Office Park, Bedfordview"                                     # hop address for Smart Technology Centre (PTY) LTD
            location = 'unknown'                                                                                   # nominatum is unable to locate this address
            y = -26.11684278
            x = 28.1578774
        if asn == '42473':  
            hop_address = "Teraco IPX, 5 Brewery St, Isando, Kempton Park, 1600, South Africa" 
            #hop_address = "Kranhaus 1, 50678 Köln, Germany"                                                         # hop address for ANEXIA Internet germany
            #location = geolocator.geocode(hop_address)
            location = 'unknown'
            y = -26.1378706
            x = 28.1987166
            

    # IF no ASN is provided check hostnames to provide geocordinates locations
    elif hostname != 'unknown':
        
        if hostname == 'jenny-internet.ixp.joburg':                                          # jenny-internet.ixp.joburg
            hop_address = "90 Oxford St, Randburg"                                           # hop address for Jenny Internet
            location = geolocator.geocode(hop_address)
            
        if hostname == '196-60-9-249.ixp.joburg':
            hop_address = "Teraco IPX, 5 Brewery St, Isando, Kempton Park, 1600, South Africa"           # hop address for Teraco (PCH NAPAfrica Johannesburg) https://www.pch.net/ixp/details/1306 (IPX)
            # location = geolocator.geocode(hop_address)                                     # nominatum is unable to locate this address
            location = 'unknown'
            y = -26.1378706
            x = 28.1987166
            

    if location == "unknown":
        # When nominatum has been unable to find a geolocation, but it has been found  manually.
        pass
    else: 
        # When nominatum found the locations
        if location != None:
            y = location.latitude
            x = location.longitude
        else:
            y = None
            x = None
    
    return x,y, hop_address
'''
# Now check distance between last location and current location
def check_distance(c_x,c_y,h_x,h_y):
    
    coords_1 = (c_y, c_x )
    coords_2 = (h_y, h_x)
    distance = geodesic(coords_1, coords_2).km
    return distance

def create_tables(): 
    sql = "DROP TABLE measurements;"
    cursor.execute(sql)
    print(cursor.rowcount,"Measurements !Table deleted.")
    mydb.commit()
    sql = "DROP TABLE probes;"
    cursor.execute(sql)
    print(cursor.rowcount,"probes !Table deleted.")
    mydb.commit()
    sql = "DROP TABLE hops;"
    cursor.execute(sql)
    print(cursor.rowcount,"hops !Table deleted.")
    mydb.commit()
    sql = "DROP TABLE asn;"
    cursor.execute(sql)
    print(cursor.rowcount,"asn !Table deleted.")
    mydb.commit()
    sql = "DROP TABLE asn_address;"
    cursor.execute(sql)
    print(cursor.rowcount,"asn_address !Table deleted.")
    mydb.commit()  
    sql = "DROP TABLE geo;"
    cursor.execute(sql)
    print(cursor.rowcount,"geo !Table deleted.")
    mydb.commit()
    cursor.execute("CREATE TABLE probes (id INT PRIMARY KEY, lat DECIMAL(10, 8), lon DECIMAL(11, 8), asn INT, ip VARCHAR(15), isanchor BOOLEAN)")
    cursor.execute("CREATE TABLE measurements (id INT PRIMARY KEY, target_id INT)")
    cursor.execute("CREATE TABLE asn (id INT PRIMARY KEY, isixp BOOLEAN, ixpname VARCHAR(40))")
    cursor.execute("CREATE TABLE hops (id INT AUTO_INCREMENT PRIMARY KEY, measurement INT, probe INT, hop INT, min_rtt FLOAT, hostname VARCHAR(120), prefix VARCHAR(20), ip_from VARCHAR(15), ip_id INT, address_id INT)")
    cursor.execute("CREATE TABLE asn_address (id INT AUTO_INCREMENT PRIMARY KEY, asn INT, holder varchar(80), address VARCHAR(200), lat DECIMAL(10, 8), lon DECIMAL(11, 8))")
    cursor.execute("create TABLE geo (id INT AUTO_INCREMENT PRIMARY KEY, ip varchar(15), lat decimal(10,8), lon decimal(11,8), address VARCHAR(200) )")
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall() ## it returns list of tables present in the database

    ## showing all the tables one by one
    for table in tables:
        print(table)

def populate_database():
    # Get all data from file    
    with open("dictionary22.json") as file:
        data =json.load(file)
    a=0
    for measurement in data:
        target_id = str(data[measurement]['probe_id'])
        target_ip = data[measurement]['target_ip']
        target_lat = data[measurement]['target_lat']
        target_lon = data[measurement]['target_lon']
        target_address = data[measurement]['target_address']
        target_isanchor = data[measurement]['target_isanchor']
        m = str(measurement)
        # Check if meaurement doesnt already exists in the database
        sql = "SELECT * FROM measurements WHERE id = %s"
        val = (m,)
        cursor.execute(sql, val)
        myresult = cursor.fetchall()

        if myresult == []:

            sql = "INSERT INTO measurements (id, target_id) VALUES (%s, %s)"
            val = (m, target_id)
        
            cursor.execute(sql,val)
            print(a, cursor.rowcount,"Measurement", m, " !record inserted.")
            mydb.commit()
        a +=1
        b = 0
        check = 0
        for probe in data[measurement]:
            #print(probe)
            if probe not in ('probe_id', 'target_ip', 'target_isanchor', 'target_lat','target_lon','target_address'):
                # Check if probe doesnt already exists in the database
                sql = "SELECT * FROM probes WHERE id = %s"
                val = (probe,)
                cursor.execute(sql, val)
                myresult = cursor.fetchall()
              
                if myresult == []:
                    #print("Probe is ", probe)
                    
                    lat = data[measurement][probe]['probe_y']
                    lon = data[measurement][probe]['probe_x']
                    asn = data[measurement][probe]['probe_asn']
                    ip = data[measurement][probe]['probe_ip']
                    
                    #  TABLE probes (id INT PRIMARY KEY, lat DECIMAL(10, 8), lon DECIMAL(11, 8), asn INT, ip VARCHAR(15))
                    sql = "INSERT INTO probes (id, lat, lon, asn, ip) VALUES (%s, %s, %s, %s, %s)"
                    val = (probe, lat, lon, asn, ip)
                    cursor.execute(sql,val)
                    #print(b, cursor.rowcount," Probe ", probe, " !record inserted.")
                    mydb.commit()
                    b +=1
                c = 0
                for hop in data[measurement][probe]: 
                    #  TABLE hops (id INT AUTO_INCREMENT PRIMARY KEY, hop INT, measurement INT, 
                    # probe INT, hostname VARCHAR(40), prefix VARCHAR(20), hop_no INT, ip_from VARCHAR(15), asn INT, lat DECIMAL(10, 8), lon DECIMAL(11, 8) )")
                    if hop not in ('probe_x', 'probe_y', 'probe_asn','probe_ip'):
                                                
                        hostname = data[measurement][probe][hop]['hostname']
                        holder = data[measurement][probe][hop]['hostname']
                        prefix = data[measurement][probe][hop]['prefix']
                        ip = data[measurement][probe][hop]['from']
                        asn = data[measurement][probe][hop]['asn']
                        min_rtt = data[measurement][probe][hop]['min_rtt']
                        if asn == "unknown" or asn == "not announced":
                            asn = 0
                        sql = "INSERT INTO hops (measurement, probe, min_rtt, hop, hostname, prefix, ip_from ) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                        val = (measurement, probe, min_rtt, hop, hostname, prefix, ip)
                        cursor.execute(sql,val)
                        #print(c, cursor.rowcount," HOP ", h, " !record inserted.")
                        mydb.commit()
                        sql = 'SELECT LAST_INSERT_ID()'
                        cursor.execute(sql)
                        hop_id = cursor.fetchone()
                        
                        print ("HOp_id is ", hop_id)
                        
                        # Get the physical address of the IP
                        print(ip)
                        address,x,y = get_location(ip)

                        print(address)
                        # if the address cannot be determined set coords to previous
                        # TODO may need to look at CGN, first one may be local and ok 
                        # but second one could be situated at the remote end and therefore
                        # instead of previous needs to be set to next. 
                        if check == 0:
                            prev_y = -26.02665740
                            prev_x = 28.01310050  
                            check = 1  
                        if address == "local" or address == 'None' or address == 'CGN':
                            y = prev_y
                            x = prev_x
                        # get the Geo coordiantes of the address
                        

                        if ip != None:    
                            # Check that ip doesnt already exist in geo table
                            sql = "SELECT id FROM geo WHERE ip = %s AND lat = %s AND lon = %s"
                            val = (ip,y,x)
                            cursor.execute(sql, val)
                            ip_id = cursor.fetchone()
                            print("ip_id IS Before", ip_id)

                            if ip_id == [] or ip_id == None:
                                sql = "INSERT INTO geo (ip, lat, lon, address) VALUES (%s, %s, %s, %s)"
                                val = (ip, y,x, address)
                                print (address)
                                cursor.execute(sql,val)
                                #print(c, cursor.rowcount," HOP ", h, " !record inserted.")
                                mydb.commit()
                                sql = 'SELECT LAST_INSERT_ID()'
                                cursor.execute(sql)
                                ip_id = cursor.fetchone()
                            
                            print("hop_id,ip_id IS after", hop_id[0],ip_id[0])
                            # Dont forget to link this ip with the hop 
                            sql = "UPDATE hops set ip_id = %s where id = %s"
                            val = (ip_id[0], hop_id[0])
                            cursor.execute(sql,val)

                                
                           


                        prev_x = x
                        prev_y = y
                        #c +=1
                        
                        # Check if ASN address doesnt already exists in the database
                        sql = "SELECT * FROM asn_address WHERE asn = %s"
                        val = (asn,)
                        cursor.execute(sql, val)
                        myresult = cursor.fetchall()
                        print("MYRESULT IS ",myresult)
                        if myresult == []:
                            id = data[measurement][probe][hop]['asn']
                            if id == 'unknown' or id == 'None' or id == 'not announced':
                                continue
                            
                            if data[measurement][probe][hop]['isixp'] == None:
                                data[measurement][probe][hop]['isixp'] == 0
                            isixp = data[measurement][probe][hop]['isixp']
                            ixpname = data[measurement][probe][hop]['ixpname']
                            
                            #Check to make sure asn doesnt already exist
                            sql = "SELECT * FROM asn WHERE id = %s"
                            val = (asn,)
                            cursor.execute(sql, val)
                            myresult = cursor.fetchall()
                            print("MYRESULT IS ",myresult)
                            if myresult != []:
                                continue

                            
                            # TABLE asn (id INT PRIMARY KEY, isixp BOOLEAN, ixpname VARCHAR(40), holder VARCHAR(80))")
                            sql = "INSERT INTO asn (id, isixp, ixpname) VALUES (%s, %s, %s)"
                            val = (id, isixp, ixpname)
                            cursor.execute(sql,val)
                            #print(b, cursor.rowcount," ASN ", id , " !record inserted.")
                            mydb.commit() 
                            
                            
                            # TABLE asn_address (id INT AUTO_INCREMENT PRIMARY KEY, asn INT, 
                            # holder varchar(40), address VARCHAR(120), lat DECIMAL(10, 8), lon DECIMAL(11, 8))") 
                            asn = data[measurement][probe][hop]['asn']
                            holder = data[measurement][probe][hop]['holder']
                            address = ""
                            lat = 0
                            lon = 0
                            sql = "INSERT INTO asn_address (asn, holder, address, lat, lon) VALUES (%s, %s, %s, %s, %s)"
                            val = (asn, holder, address, lat, lon)
                            cursor.execute(sql,val)
                            #print(b, cursor.rowcount," ASN Address", asn , " !record inserted.")
                            mydb.commit() 
   
    for measurement in data:
        target_id = str(data[measurement]['probe_id'])
       
        target_isanchor = data[measurement]['target_isanchor']
        
        sql = "UPDATE probes SET isanchor = %s WHERE id = %s "
        val = (target_isanchor, target_id)
    
        cursor.execute(sql,val)
        print(cursor.rowcount,"Probe", target_id, " !record inserted.", target_isanchor)
        mydb.commit()

    # UPDATE hops with relevant address
    sql = "select * from hops"
    cursor.execute(sql)
    hops = cursor.fetchall()
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
        if asn_address == None:
            continue
        address_id = asn_address[0] 
        sql = "UPDATE hops SET address_id = %s WHERE id = %s"
        val = (address_id, hop_id)
        cursor.execute(sql,val)
        mydb.commit() 
        print(val)

       
             

if __name__ == "__main__":
    
    

    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="brindle7",
    database="ipgeo"
    )
    cursor = mydb.cursor(buffered=True)

    # Create the tables
    if create_table:
        create_tables()
    # read in the data from file created by create-measurements and populate db
    if read_file:
        populate_database()

    # The following sql statement selects all measurement where the target is an anchor
    # select * from measurements,probes where target_id=probes.id AND probes.isanchor=1 ;

    '''
    sql = "Select * from probes"
         
    cursor.execute(sql)
    print(cursor.rowcount,"Probes table read.")
    probes = cursor.fetchall()

    for probe in probes:
        probe_id = probe[0]
        probe_lat = probe[1]
        probe_lon = probe[2]
        probe_asn = probe[3]
        probe_ip = probe[4]
        print(probe_lat)
        sql = "Select * from hops where ip_from = %s"
        val = (probe_ip,)
         
        cursor.execute(sql,val)
        print(cursor.rowcount,"hops table read.")
        hops = cursor.fetchall()
        for hop in hops:
            print (hop)
'''
    




