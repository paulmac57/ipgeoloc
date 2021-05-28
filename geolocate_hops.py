# Reads Hops from database and attempts to locate the geocordinates of them
# then enters the lat, lon and address back into the geo table  

import mysql.connector
import json
from geopy.geocoders import Nominatim
from html_create_tr import Html_Create 
from geopy.distance import geodesic

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="brindle7",
    database="ipgeo"
    )
cursor = mydb.cursor()
geolocator = Nominatim(user_agent="aswindow")

# Converts the list which is loaded from the file onto a dictionary
def Convert(lst):
    res_dct = {lst[i]: lst[i + 1] for i in range(0, len(lst), 2)}
    return res_dct

# If an ASN is provided get corordinates from known LOCAL address of that ASN
def check_location(asn,holder,hostname):
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

# Choose the emasurements we are interseted in
measurements = { 28761928:
  6053,
  28761929:
  6176,
  28761930:
  6179,
  28761932:
  6187,
  28761933:
  6569,
  28761934:
  6777,
  28761935:
  6779
}
m_dict = {}
for measurement in measurements:
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

        x,y,address = check_location(id[8],ids[2],id[5]) # asn, holder, hostname

        print(x,y,address)
    
    print(m_dict[measurement][1000237])



    

      


    
    #hops_dict = Convert(hops)
    #print (hops_dict)