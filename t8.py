from ipwhois import IPWhois
from pprint import pprint
import geocoder
import re
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="aswindow")
import json
import os
k = os.environ.get('GOOGLE_API_KEY') 

ip = '188.172.217.85'
#ip = '41.191.219.216'
ip = '63.223.48.21'
obj = IPWhois(ip)
results = obj.lookup_rdap(depth=1)
    
r = results['objects'].keys()
# TODO above may return multiple addresses so create a
# Sense check vs Speed of light
# to decide which one is best
# for now just use first address

region = list(r)
print('regions are',region)
#print(results['objects'])
#print(results['objects']['ORG-AIG10-RIPE']['contact']['address'][0]['value'])
#[region]['contact']['address'])
c=0
coord_flag = False
for a in region:
    print (a)
    print(results['objects'][a]['contact']['address'])
    if results['objects'][a]['contact']['address'] != None:
        add = results['objects'][a]['contact']['address']
        
        addresses = list(add)
        '''
        print("add **********",add)
        print("addresses ***********",addresses)
        print ('==========================================================')
        '''
        for b in range(len(addresses)):
            # print( results['objects'][a]['contact']['address'][b]['value'])
            this_add = results['objects'][a]['contact']['address'][b]['value']
            this_add = re.sub('\n', ' ',this_add.rstrip())
            print("address is",this_add)
            if this_add != "None":
                location = geolocator.geocode(this_add)
                print("location is ",location)
                if location == None :
                    
                    g = geocoder.google(this_add, key = k)
                    if g != None:
                        x = g.lng
                        y = g.lat
                        print (x,y, " got from GOOGLE")
                        coord_flag = True
                        break
                    
                else:
                    x = location.longitude
                    y = location.latitude
                    print (x,y, " got from nominatum")
                    coord_flag = True
                    break
            
    if coord_flag == True:
        coord_flag == False
        #break

