import mysql.connector
import json
from geopy.geocoders import Nominatim
from html_create_tr import Html_Create 
from geopy.distance import geodesic
from ipwhois import IPWhois
from pprint import pprint

geolocator = Nominatim(user_agent="aswindow")

address={}
#print (dir(ipwhois.IPWhois))
obj = IPWhois('169.255.0.129')
results = results = obj.lookup_rdap(depth=1)
#pprint(results)
print(results['objects']['DT19-AFRINIC']['contact']['address'][0]['value'])

'''   
if ip.startswith("10") or ip.startswith(('17.16','17.17','17.18','17.19','17.20','17.21','17.22','17.23','17.24','17.25','17.26','17.27','17.28','17.29','17.30','17.31')) or ip.startswith("192.168"):
    address = "local"
else:
    #address_dict = ipwhois.rdap   rdap(ip)
    #address_dict)
    #get_address('169.255.0.129')
'''
