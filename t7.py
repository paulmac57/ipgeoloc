import json
from geopy.geocoders import Nominatim
from html_create_tr import Html_Create 
from geopy.distance import geodesic
from ipwhois import IPWhois
from pprint import pprint
import geocoder
import requests
import os

k = os.environ.get('GOOGLE_API_KEY')

g = geocoder.google('21 Landmarks Avenue, Centurion 0187 Johannesburg, South Africa', key = k)
print (g.latlng)

'''
url = 'https://maps.googleapis.com/maps/api/geocode/json'
params = {'sensor': 'false', 'address': '21 Landmarks Avenue Centurion 0187 Johannesburg, South Africa', 'key': k}
r = requests.get(url, params=params)
results = r.json()['results']

print(results)




geolocator = Nominatim(user_agent="aswindow")

address = 'Hostus, South Africa'
location = geolocator.geocode(address)

print(location)
'''