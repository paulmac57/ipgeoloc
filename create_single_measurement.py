# TODO REMOVE The Safeguard before running again (dont want to create more unneccessary traceroute on ATLAS) at line 94
# TODO Set the probes_measurement_id to the emasurement containg the probes you want to use
# TODO Change the filename below

probes_measurement_id = 28380424
filename = 'measurements/south_africa_measurements.json'


from datetime import datetime
import json 
import os

# Gets the required measuremnt from RIPE ATLAS and creates the initial dictionary file 

# info from https://ripe-atlas-cousteau.readthedocs.io/_/downloads/en/latest/pdf/
from ripe.atlas.cousteau import Ping, Traceroute, AtlasSource, AtlasRequest, AtlasCreateRequest, AtlasLatestRequest, Probe, Measurement
# Sagans sole purpose is to make RIPE Atlas measurements manageable from within Python.
# https://ripe-atlas-sagan.readthedocs.io/en/latest/use.html#how-to-use-this-library
# Attributes and Methods at https://ripe-atlas-sagan.readthedocs.io/en/latest/types.html
measurement = Measurement(id=28380424)


from ripe.atlas.sagan import Result, TracerouteResult
# Opensource Geocoder
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="aswindow")
# A Python library to gather IP address details (ASN, prefix, resource holder, reverse DNS) using the RIPEStat API,
# with a basic cache to avoid flood of requests and to enhance performances. https://pypi.org/project/ipdetailscache/
#from pierky.ipdetailscache import IPDetailsCache
#cache = IPDetailsCache()
#cache.UseIXPs()
#r = cache.GetIPInformation( "193.0.6.139" ) # example use
#print (r)
# target_address = "90 Oxford Street, Randburg"   # sample target address
# Discover the geo cordinates of the target location
#location = geolocator.geocode(target_address)
#print(location)
#latitude = location.latitude
#longitude = location.longitude
#print ("lat is ", location.latitude)
#print ("lon is ", location.longitude)
        
ATLAS_API_KEY = "6f0e691d-056c-497d-9f5b-2297e970ec60"
traceroute_dict = {}                                        # initialis the measuretments dictionary
measurements_list = [28380424,]                               # initialise the measurements list
from html_create import Html_Create 

# Get a list of the probes to be used, easiset to get list from first measurement which used all probes in South Africa.

for measurement in measurements_list:                       # Its unlikely I will ever use more than 1 measurement but just in case
    m = Measurement(id=measurement)                         # get metadata for this measurement
    kwargs = {
    "msm_id": measurement,   # my south africa measurement 
    #"start": datetime(2015, 05, 19), # just testing date filtering
    #"stop": datetime(2015, 05, 20),  # just testing date filtering
    #"probe_ids": [1000070]  # the first probe in the measurement
    }
    is_success, results = AtlasLatestRequest(**kwargs).create()
probes =[]
# probes =[6779,6539,4070,13888,35743,12205,50518,19994,1000825]
measurements = []

print(results)
'''

for probe in results:
    probes.append(probe['prb_id'])


# now carry out a traceroute to each probe(target) from every other probe (landmark)
print(results)

for target in results: 
    target_probe_id = target['prb_id'] 
    probe = Probe(id=target_probe_id) 
    
    target_ip =  probe.address_v4 
    t = str(target_ip) 
    
    desc = "2 Traceroute to "+ t + " at "+ str(target_probe_id)
    print(desc)
    # Remove all landmarks that dont have an public IP address.
    
    #target_ip = None # TODO REMOVE This Safeguard before running again (dont want to create more unneccessary traceroute on ATLAS)
    
    if target_ip == None:
        continue 

    traceroute = Traceroute(af = 4, target=target_ip, description=desc, protocol ="ICMP")
    source = AtlasSource(requested=66, type="msm", value=probes_measurement_id)
   
    atlas_request = AtlasCreateRequest(
    key=ATLAS_API_KEY,
    measurements=[traceroute],
    sources=[source],
    is_oneoff=True)
    (is_success, response) = atlas_request.create()
    print(desc,is_success,response) 


    measurements.append(response['measurements'][0])
    measurements.append(target_probe_id)
# measurements =  ', '.join(map(str, measurements))
# create file of measurement,target_probe_id,......,..........
with open(filename, 'w') as outfile:
    json.dump(measurements, outfile)

'''
 