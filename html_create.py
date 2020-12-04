import pprint
import os
import time
import collections
import sys

from geopy.geocoders import Nominatim
import ipinfo

class Html_Create:
    def create_html(self, target_ip):
        # write default head info to new file
        filename = 'targets/target_'+str(target_ip)+'.html'
        cmd2 = 'chmod ' +'766 '+filename
        cmd = 'cp html/head.html '+ filename
                
        os.system(cmd)
        # Fix File Permisssions
        os.system(cmd2)
                
        # Write latitude and longitude to html file for zoom location
        # open file 
        ip = open(filename, 'a')
        destination_address = self.measurement_dict[self.measurement_id]['dest_addr']
        destination_asn = self.measurement_dict[self.measurement_id]['dest_asn']
        print(self.measurement_dict[self.measurement_id]['target_coords'][1])
        target_latitude = self.measurement_dict[self.measurement_id]['target_coords'][1][0]
        target_longitude = self.measurement_dict[self.measurement_id]['target_coords'][1][1]
        target_address = self.measurement_dict[self.measurement_id]['target_coords'][0]
        del self.measurement_dict[self.measurement_id]['dest_addr']
        del self.measurement_dict[self.measurement_id]['dest_asn']
        del self.measurement_dict[self.measurement_id]['target_coords']


        # TODO: work out a way of zooming to the correct distance 
        highlat = -90
        lowlat = 90
        highlon = -180
        lowlon =  180
        for key in self.measurement_dict[self.measurement_id].keys():
            print(key)
            rtt = self.measurement_dict[self.measurement_id][key]['rtt'] 
            #print ("RTT IS ",rtt)
            lon = self.measurement_dict[self.measurement_id][key]['x_coord']
                     
            lat = self.measurement_dict[self.measurement_id][key]['y_coord']
            ip_address = self.measurement_dict[self.measurement_id][key]['ip_addr']
            
            # Work out approximate middle of area to display map
            if lat > highlat:
                highlat = lat
            if lat < lowlat:
                lowlat = lat   
            if lon > highlon:
                highlon = lon
            if lon < lowlon:
                lowlon = lon
            print(highlat,lowlat,highlon,lowlon)
        
        lat = lowlat+ ((highlat - lowlat)/2)
        lon = lowlon+ ((highlon - lowlon)/2)
        ip.write(str(lat)+", "+str(lon)+'], 8);\n')
        ip.close()
        ###########################################################

        # write tilelayer information to html file
        cmd = 'cat html/tilelayer.html >> '+ filename
        os.system(cmd)


        
        ip = open(filename, 'a')
        

        # create ipaddress points on map in green circles
        stringa = "      var circle"
        stringb = " = L.circle(["
        string1 = "      // show the area of operation of the AS on the map\n      var polygon = L.polygon([\n"
        string2 = "], { color: 'green', fillColor: '#00', interactive: false, fillOpacity: 0.0, radius: "
        string21 = "], { color: 'green', fillColor: '#8000000', fillOpacity: 0.5, radius: "
        string22 = "], { color: 'blue', fillColor: '#8000000', fillOpacity: 0.5, radius: "
        string23 = "], { color: 'red', fillColor: '#00', interactive: false, fillOpacity: 0.0, radius: "
        string24 = "], { color: 'red', fillColor: '#8000000', fillOpacity: 0.5, radius: "
        string25 = "], { color: 'yellow', fillColor: '#8000000', fillOpacity: 0.5, radius: "
        string2a = " }).addTo(map);"


        string3 = "        ]).addTo(map);\n"
        string4 = '      polygon.bindPopup("<b>AS'
        string5 = '</b><br />'
        string6 = '<br />Area of Operation");\n'
        string7 = '      circle.bindPopup("<b>Probe '
        string7a ='      circle'
        string7b ='.bindPopup("<b>Probe '
        string7c ='.bindPopup("<b>Target '
        string8 = ' ").openPopup();\n\n'
        string8a = ' ");\n\n'
        spacer1 = "        ["
        spacer2 = "],\n"
        
        #Calculate the probe with the shortest ping
        shortest_rtt = 100
        for key in self.measurement_dict[self.measurement_id].keys():
            rtt = self.measurement_dict[self.measurement_id][key]['rtt']                # return trip time
            if rtt != None:                                                             # If probe didnt return a trip time then ignore
                if rtt < shortest_rtt:
                    shortest_rtt = rtt
                    shortest_probe = key

        # show all landmarks on map
        i = 0
        for key in self.measurement_dict[self.measurement_id].keys():
            #print(key)
            i = i+2
            rtt = self.measurement_dict[self.measurement_id][key]['rtt']                # return trip time
            lon = self.measurement_dict[self.measurement_id][key]['x_coord']
                     
            lat = self.measurement_dict[self.measurement_id][key]['y_coord']
            ip_address = self.measurement_dict[self.measurement_id][key]['ip_addr']
            asn = self.measurement_dict[self.measurement_id][key]['asn']
            
                
            ip = open(filename, 'a')

            #calculate topgrapical distance to target (ie radius of circle)
            speed =  .66 * 300000                                           # Average Speed of packet though fibre cable 2/3C  = 200 km per millisecond
            if rtt != None:                                                 # If probe didnt return a trip time then ignore
                stt = rtt/2                                                 # Single trip time
                if stt <= 5:                                                # Only use landmarks that are within 5ms topologically = 1000 km geographically Max
                    distance = stt * speed                                  # Distance packet travelled at this speed                          
                    print("probe is ", key," AS is", asn,"rtt is ",rtt,"Distance to target is ", distance)

                    if key == shortest_probe:                                # If this is the probe with the shortest ping highlight it in red
                        # Create Shortest_probe Radius in RED
                        ip.write(stringa + str(i)+stringb+str(lat)+ ','+str(lon)+string23+str(distance)+string2a+'\n')
                        # Create RED Probe location - These is the probe with the shortest ping
                        ip.write(stringa + str(i+1)+stringb+str(lat)+ ','+str(lon)+string24+str(1000)+string2a+'\n')  
                        # Create shortewst ping Probe Popup
                        ip.write(string7a +str(i+1)+string7b+str(key) + string5 + 'AS '+str(asn)+"<br />" + str(ip_address) + "<br />" + "STT: "+str(stt) +string8)
                        print("KEY IS ", key)
                    else:
                        # Create Green probe Radius
                        ip.write(stringa + str(i)+stringb+str(lat)+ ','+str(lon)+string2+str(distance)+string2a+'\n')
                        # Create Green Probe location - These are probes used in the calculation
                        ip.write(stringa + str(i+1)+stringb+str(lat)+ ','+str(lon)+string21+str(500)+string2a+'\n')  
                        # Create Probe Popup
                        ip.write(string7a +str(i+1)+string7b+str(key) + string5 + 'AS '+str(asn)+"<br />" + str(ip_address) + "<br />" + "STT: "+str(stt) +string8a)
                else:                                                       # If probes single trip time was over 5 ms then create a blue marker 
                                                                            # but dont utilise in calculations
                    # Create Blue Probe location - This is to show Probes which were not used as they were topologically too far away
                    ip.write(stringa + str(i+1)+stringb+str(lat)+ ','+str(lon)+string22+str(500)+string2a+'\n')  
                    # Create Probe Popup
                    ip.write(string7a +str(i+1)+string7b+str(key) + string5 + 'AS '+str(asn)+"<br />" + str(ip_address) + "<br />" + "STT: "+str(rtt/2)+string8a)

        #Show Actual target Coordinates for comparison 

        # Create Actual Target location - This is for comparison only
        ip.write(stringa + str(i+3)+stringb+str(target_latitude)+ ','+str(target_longitude)+string25+str(250)+string2a+'\n') 
        ip.write(string7a +str(i+3)+string7c+ str(target_ip) +"<br />" + str(target_address) +string8a)




        # Complete Script and write to file
        #ip.write(string7 +'asnumber'+string5+'owner'+string8)
        string9 = "    </script>\n  </body>\n</html>"
        ip.write (string9)
        ip.close()


        print (filename+ " Written Succesfully, copy it to your webserver")
        
    def __init__(self, measurement_dict):
        measurement_list = list(measurement_dict.keys())                       
        self.measurement_id = measurement_list[0]                                  # only one measurement should have been passed 
        self.target = measurement_dict[self.measurement_id]['dest_addr']
        self.measurement_dict = measurement_dict
        #self.handler = ipinfo.getHandler(access_token='5887e8b74e7139')
        
        #self.url_base = 'http://ipinfo.io/'
        #print ("this is the target "+ self.target)
        self.create_html(self.target)

if __name__ == "__main__":
    os.chdir('/home/paul/Documents/ipgeoloc')
    IP = ''
    result = {}
    thistarget = target(IP)
    #print (thisas.get_company_info())
    #print (thisas.get_ipinfo())