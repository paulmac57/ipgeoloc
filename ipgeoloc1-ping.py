
# info from https://ripe-atlas-cousteau.readthedocs.io/_/downloads/en/latest/pdf/
from ripe.atlas.cousteau import AtlasLatestRequest, Probe, Measurement
# Sagans sole purpose is to make RIPE Atlas measurements manageable from within Python.
# https://ripe-atlas-sagan.readthedocs.io/en/latest/use.html#how-to-use-this-library
# Attributes and Methods at https://ripe-atlas-sagan.readthedocs.io/en/latest/types.html
from ripe.atlas.sagan import Result, PingResult
from geopy.geocoders import Nominatim
from html_create import Html_Create 
geolocator = Nominatim(user_agent="aswindow")
target_address = "90 Oxford Street, Randburg"   # sample target address

location = geolocator.geocode(target_address)

print(location)

latitude = location.latitude
longitude = location.longitude
print ("lat is ", location.latitude)
print ("lon is ", location.longitude)
        

measurements_dict = {}                                        # initialise the measuretments dictionary
measurements_list = [28110368,]                               # initialise the measurements list



for measurement in measurements_list:

    m = Measurement(id=measurement)                         # get metadata for this measurement


    
    kwargs = {
    "msm_id": measurement,   # my south africa measurement 
    #"start": datetime(2015, 05, 19), # just testing date filtering
    #"stop": datetime(2015, 05, 20),  # just testing date filtering
    #"probe_ids": [1000070]  # the first probe in the measurement

    }
    is_success, results = AtlasLatestRequest(**kwargs).create()
    if is_success:                                          # if measuremnt was a success
        measurements_dict[measurement] = {}                 # initialis this measurements dictionary
        probes = {}                                         # initialise all the probes dictionaries within this measurement
        i = 0
        for result in results:                              # get all the results of the pings from landmarks to target
            print("Reading measurement data, ",measurement, "from probes ", i," one moment")
            # print("this is result ",i, "of measuremnt ", measurement)

            result = PingResult(result) 
                             
            p = result.probe_id
            probe = Probe(id=p)                                                     # Get all the properties of the individual probe used in this individual measurement 
            a = probe.geometry['coordinates']                                       # Create a list of Coordinates
            probe_x = a[0]                                                          # Probes X coordinate
            probe_y = a[1]                                                          # Probes Y coordinate
            probe_id = result.probe_id                                              # get the probe_id for this individual measurement
            measurements_dict[measurement][probe_id] = {}                           # initialise this probes dictioonary
            measurements_dict[measurement][probe_id]['rtt'] = result.rtt_min        # get the minimum RTT measurement of the 3 pings from this probe
            measurements_dict[measurement][probe_id]['ip_addr'] = result.origin     # get the Ip address of this probe
            measurements_dict[measurement][probe_id]['x_coord'] = probe_x           # get the x coordinate of this probe
            measurements_dict[measurement][probe_id]['y_coord'] = probe_y           # get the y coordinate of this probe
            measurements_dict[measurement][probe_id]['asn'] = probe.asn_v4
        

           

            i=i+1
        measurements_dict[measurement]['dest_addr'] = m.target_ip                   # Add the Target IP address for this measurement to the Dictionary
        measurements_dict[measurement]['dest_asn'] = m.target_asn                   # Add the Target ASN for this measurement if it is available.
        measurements_dict[measurement]['target_coords'] = location                   # Add the Target Coordinates for this measurement if it is available.
        #print(measurements_dict.keys())
        #print(measurements_dict)
        #print(measurements_dict[measurement]['dest_addr'])
        html = Html_Create(measurements_dict)
      
        
        
        