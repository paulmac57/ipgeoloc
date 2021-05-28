# Gets the required measuremnt from RIPE ATLAS and creates the initial dictionary file 

# A Python library to gather IP address details (ASN, prefix, resource holder, reverse DNS) using the RIPEStat API,
# with a basic cache to avoid flood of requests and to enhance performances. https://pypi.org/project/ipdetailscache/

from pierky.ipdetailscache import IPDetailsCache
cache = IPDetailsCache(IP_ADDRESSES_CACHE_FILE = "cache/ip_addr.cache", IP_PREFIXES_CACHE_FILE = "cache/ip_pref.cache", MAX_CACHE = 604800, Debug = False )

# info from https://ripe-atlas-cousteau.readthedocs.io/_/downloads/en/latest/pdf/
from ripe.atlas.cousteau import AtlasLatestRequest, Probe, Measurement
# Sagans sole purpose is to make RIPE Atlas measurements manageable from within Python.
# https://ripe-atlas-sagan.readthedocs.io/en/latest/use.html#how-to-use-this-library
# Attributes and Methods at https://ripe-atlas-sagan.readthedocs.io/en/latest/types.html
from ripe.atlas.sagan import Result, TracerouteResult
# Opensource Geocoder
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="aswindow")
import json

# Converts the list which is loaded from the file onto a dictionary
def Convert(lst):
    res_dct = {lst[i]: lst[i + 1] for i in range(0, len(lst), 2)}
    return res_dct
         
# Driver code

#from html_create import Html_Create 



# Load the Measurements and target probe id's
with open("measurements/anchors.json") as file:
    measurements_file =json.load(file)
# convert the list into a dictionary
measurements_dict = Convert(measurements_file)
traceroute_dict = {}                                        # initialis the measuretments dictionary
# measurements_list = [28380424,]                           # this was the initial South Africa measurement, the list of probes from this are used in further measurements

# read in each measurment
for measurement in measurements_dict:                 # for each measurement
    # get the measurement ID
    print('Measurement',measurement,'Probe ',measurements_dict[measurement])
    m = Measurement(id=measurement)                         # get metadata for this measurement
    p = Probe(id=measurements_dict[measurement])                                                     # Get all the properties of the individual probe used in this individual measurement 
    coords = p.geometry['coordinates']
    coords_str = ','.join([str(elem) for elem in coords]) 
    
    print(coords_str)  
                                        # Create a list of Coordinates
     
    # Discover the physical address of the target location
    try:
        location = geolocator.reverse(coords_str)
    except:
        location = "unknown"
    print(location)
    latitude = p.geometry['coordinates'][1]
    longitude = p.geometry['coordinates'][0]
    is_anchor = p.is_anchor
    print("probe", measurements_dict[measurement],"is anchor",is_anchor)
    target_address = location
    target_probe_id = measurements_dict[measurement]
    print (measurement)    
    
    kwargs = {
    "msm_id": measurement,   # my south africa measurement 
    #"start": datetime(2015, 05, 19), # just testing date filtering
    #"stop": datetime(2015, 05, 20),  # just testing date filtering
    #"probe_ids": [1000070]  # the first probe in the measurement

    }
    is_success, results = AtlasLatestRequest(**kwargs).create()
    print (results)
    if is_success:                                              # if measuremnt was a success
        traceroute_dict[measurement] = {}                       # initialis this measurements dictionary
        traceroute_dict[measurement]["probe_id"] = target_probe_id
        traceroute_dict[measurement]["target_ip"] = m.target_ip # set target ip address
        traceroute_dict[measurement]["target_lat"] = latitude   # set target latitude
        
        traceroute_dict[measurement]["target_lon"] = longitude # set target longiyude
        traceroute_dict[measurement]["target_address"] = target_address # set target geo address
        traceroute_dict[measurement]["target_isanchor"] = is_anchor   # True if probe is anchor
        probes = {}                                             # initialise all the probes dictionaries within this measurement
        i = 0
        for result in results:                                   # get all the results of the pings from landmarks to target
            print("Reading measurement data, ",measurement, "from probes ", i," one moment")
            print("this is result ",i, "of measuremnt ", measurement)

            result = TracerouteResult(result) 
            print (result)
            if not result.is_error:                                                      # if no error in handling/parsing this result
                p = result.probe_id
                probe = Probe(id=p)                                                     # Get all the properties of the individual probe used in this individual measurement 
                print('Probe ',p)
                a = probe.geometry['coordinates']                                       # Create a list of Coordinates
                probe_x = a[0]                                                          # Probes X coordinate
                probe_y = a[1]                                                          # Probes Y coordinate
                probe_id = result.probe_id                                              # get the probe_id for this individual measurement
                if probe_id == '1000492':
                    print("HERE ITS IS *************************", probe_id, probe_x,probe_y)
                traceroute_dict[measurement][probe_id] = {}
                traceroute_dict[measurement][probe_id]['probe_x'] = probe_x
                traceroute_dict[measurement][probe_id]['probe_y'] = probe_y
                traceroute_dict[measurement][probe_id]['probe_asn'] = probe.asn_v4
                traceroute_dict[measurement][probe_id]['probe_ip'] = probe.address_v4
                hops = result.total_hops
                
                for hop in range(hops):
                    traceroute_dict[measurement][probe_id][hop+1] = {}
                    packets = result.hops[hop].packets
                                   
                    print ("Hop ", hop+1)
                    rtt_min = 100
                    pack = 0
                    traceroute_dict[measurement][probe_id][hop+1]['from'] = None
                    # Get the smallest rtt time of the 3 packets sent
                    for packet in packets:
                        
                        pack = pack + 1
                        #traceroute_dict[measurement][probe_id][hop+1][pack] = {}
                        #print("packet rtt = ",packet.rtt)
                        if packet.rtt is not None:
                            if packet.rtt < rtt_min:
                                rtt_min = packet.rtt
                                traceroute_dict[measurement][probe_id][hop+1]['from'] = packet.origin
                        #print("packet min = ",rtt_min)
                        
                    if traceroute_dict[measurement][probe_id][hop+1]['from'] is not None: 
                        traceroute_dict[measurement][probe_id][hop+1]['min_rtt'] = rtt_min
                        print(traceroute_dict[measurement][probe_id][hop+1]['from'])
                        r = cache.GetIPInformation(traceroute_dict[measurement][probe_id][hop+1]['from'])
                        traceroute_dict[measurement][probe_id][hop+1]['asn'] = r['ASN']
                        traceroute_dict[measurement][probe_id][hop+1]['hostname'] = r['HostName']
                        traceroute_dict[measurement][probe_id][hop+1]['prefix'] = r['Prefix']
                        traceroute_dict[measurement][probe_id][hop+1]['isixp'] = r['IsIXP']
                        traceroute_dict[measurement][probe_id][hop+1]['ixpname'] = r['IXPName']
                        traceroute_dict[measurement][probe_id][hop+1]['holder'] = r['Holder']
                    else:
                        traceroute_dict[measurement][probe_id][hop+1]['min_rtt'] = 100
                        traceroute_dict[measurement][probe_id][hop+1]['asn'] = 'unknown'
                        traceroute_dict[measurement][probe_id][hop+1]['hostname'] = 'unknown'
                        traceroute_dict[measurement][probe_id][hop+1]['prefix'] = 'unknown'
                        traceroute_dict[measurement][probe_id][hop+1]['isixp'] = 'unknown'
                        traceroute_dict[measurement][probe_id][hop+1]['ixpname'] = 'unknown'
                        traceroute_dict[measurement][probe_id][hop+1]['holder'] = 'unknown'
                   
                        

                    
                    
                          
                
                
                
            

           

            i=i+1
        
'''
for measurement in measurements:
    for probe in list(traceroute_dict[measurement].keys()):
        print (probe)
'''




with open("anchors_dict.json","w") as file:
    file.write(json.dumps(traceroute_dict))

#print(traceroute_dict)
#print(list(traceroute_dict[measurement].keys()))
        #print(measurements_dict[measurement]['dest_addr'])
        #html = Html_Create(measurements_dict)
      
        
        
        