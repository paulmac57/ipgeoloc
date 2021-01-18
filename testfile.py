
# Filters the list of probes by specific RTT then find Physical addresses, distances, latitude and longitude of hops
import json
from geopy.geocoders import Nominatim
from html_create_tr import Html_Create 
from geopy.distance import geodesic

geolocator = Nominatim(user_agent="aswindow")
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


# Now check distance between last location and current location
def check_distance(c_x,c_y,h_x,h_y):
    
    coords_1 = (c_y, c_x )
    coords_2 = (h_y, h_x)
    distance = geodesic(coords_1, coords_2).km
    return distance

if __name__ == "__main__":

    # Get all data from file 
    with open("dictionary.json") as file:
        data =json.load(file)

    # get the measurement ID
    measurements = list(data.keys())
    measurement  = measurements[0]

    probes = {}
    p=0
    probes['target_ip'] = data[measurement]['target_ip']
    probes['target_lat'] = data[measurement]['target_lat']
    probes['target_lon'] = data[measurement]['target_lon']
    probes['target_address'] = data[measurement]['target_address']   
    print(probes)
    for probe in data[measurement].keys():
        
        
        if probe not in ('target_ip','target_address', 'target_lat', 'target_lon'):
            hops = 0
            total_rtt = 0
            
            for hop in data[measurement][probe]:
            
                
                if hop not in ('probe_x', 'probe_y', 'probe_asn','probe_ip'):
                    hops = hops +1
                    if data[measurement][probe][hop]['hostname'] == '':
                        data[measurement][probe][hop]['hostname'] = 'unknown'
                    # Not required its is not the addition of the hop times, just simply the time of the last hop           
                    # total_rtt = (data[measurement][probe][hop]['min_rtt']) + total_rtt
                    total_rtt =  data[measurement][probe][hop]['min_rtt']  
                    # Check to see if all hops can be located
                    hop_x,hop_y,hop_address = check_location(data[measurement][probe][hop]['asn'],data[measurement][probe][hop]['holder'],data[measurement][probe][hop]['hostname'])  
                    # if hop cannot be located then set hop so high that it will not be included in creating the html
                    if hop_x == None:
                        total_rtt = 100
                        break
            data[measurement][probe][hop]['nmb_hops'] = hops
            
            # Only use landmarks that are within 5ms return trip time topologically = 500 km one way geographically Max                      
            # Average Speed of packet though fibre cable 2/3C  = 200 km per millisecond
               
            if total_rtt <= 5:
                p= p+1
                print("Probe ", p)
                                
                probes[probe] = {}
                
                probes[probe]['probe_asn']      =   data[measurement][probe]['probe_asn']
                probes[probe]['probe_ip']       =   data[measurement][probe]['probe_ip']
                probes[probe]['probe_x']        =   data[measurement][probe]['probe_x']
                probes[probe]['probe_y']        =   data[measurement][probe]['probe_y']
                probes[probe]['Hops']           =   hops
                probes[probe]['total_rtt']      =   total_rtt
                probes[probe]['dest_address']   =   data[measurement]['target_ip']

                print ( "Probe ",probe, 
                        'ASN', probes[probe]['probe_asn'],
                        'IP', probes[probe]['probe_ip'],
                        'X',  probes[probe]['probe_x'],
                        'Y',  probes[probe]['probe_y'])
                # Keep track of distances
                current_x = probes[probe]['probe_x']
                current_y = probes[probe]['probe_y']
                
                for h in data[measurement][probe].keys():
                    if h not in ('probe_x', 'probe_y', 'probe_asn','probe_ip'):
                        print('hop',h)
                        probes[probe][h] = {}
                        probes[probe][h]['asn']        =   data[measurement][probe][h]['asn']
                        probes[probe][h]['from']       =   data[measurement][probe][h]['from']      
                        probes[probe][h]['prefix']     =   data[measurement][probe][h]['prefix']
                        probes[probe][h]['hostname']   =   data[measurement][probe][h]['hostname']
                        probes[probe][h]['holder']     =   data[measurement][probe][h]['holder']
                        probes[probe][h]['min_rtt']    =   data[measurement][probe][h]['min_rtt'] 
                        print ( 'ASN',      probes[probe][h]['asn'],
                                'From',     probes[probe][h]['from'],      
                                'Prefix',   probes[probe][h]['prefix'],
                                'Hostname', probes[probe][h]['hostname'],
                                'Holder',   probes[probe][h]['holder'],
                                'Min-RTT',  probes[probe][h]['min_rtt'] )
                        hop_x,hop_y,hop_address = check_location(probes[probe][h]['asn'],probes[probe][h]['holder'],probes[probe][h]['hostname'])
                        print ("lat is ", hop_y,"lon is ", hop_x)
                        print(hop_address)
                        hop_distance = check_distance(current_x, current_y, hop_x,hop_y)
                        probes[probe][h]['hop_longitude'] = hop_x
                        probes[probe][h]['hop_latitude'] = hop_y
                        probes[probe][h]['address'] = hop_address
                        probes[probe][h]['distance'] = hop_distance
                        current_x = hop_x
                        current_y = hop_y
                    
                

                
                print('Hops',       probes[probe]['Hops'],
                    'total_rtt',  total_rtt)
                print('Destination', probes[probe]['dest_address'])
                print('==============================================================')
            
    import json 
    
    # Create a testfile so dont have to keep interrogating RIPE ATLAS
    with open("probes.json","w") as file:
        file.write(json.dumps(probes))           

     # When Live Call html_create with new probe info   
    #html = Html_Create(probes)


