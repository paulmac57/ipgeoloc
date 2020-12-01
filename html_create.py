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
        del self.measurement_dict[self.measurement_id]['dest_addr']
        del self.measurement_dict[self.measurement_id]['dest_asn']

        #print (self.measurement_dict[self.measurement_id].keys())

        # TODO: work out a way of zooming to the correct distance 
        highlat = -90
        lowlat = 90
        highlon = -180
        lowlon =  180
        for key in self.measurement_dict[self.measurement_id].keys():
            print(key)
            rtt = self.measurement_dict[self.measurement_id][key]['rtt'] 
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


        # show the AS on the map as a large red circle at correct coordinates
        ip = open(filename, 'a')
        

        # create ipaddress points on map in green circles
        stringa = "      var circle"
        stringb = " = L.circle(["
        string1 = "      // show the area of operation of the AS on the map\n      var polygon = L.polygon([\n"
        string2 = "], { color: 'green', fillColor: '#00ff4d', fillOpacity: 0.5, radius: 20000 }).addTo(map);"
        string3 = "        ]).addTo(map);\n"
        string4 = '      polygon.bindPopup("<b>AS'
        string5 = '</b><br />'
        string6 = '<br />Area of Operation");\n'
        string7 = '      circle.bindPopup("<b>Probe '
        string7a ='      circle'
        string7b ='.bindPopup("<b>Probe '
        string8 = ' ").openPopup();\n\n'
        spacer1 = "        ["
        spacer2 = "],\n"
        




        # show all landmarks on map
        i = 0
        for key in self.measurement_dict[self.measurement_id].keys():
            print(key)
            i = i+1
            rtt = self.measurement_dict[self.measurement_id][key]['rtt'] 
            lon = self.measurement_dict[self.measurement_id][key]['x_coord']
                     
            lat = self.measurement_dict[self.measurement_id][key]['y_coord']
            ip_address = self.measurement_dict[self.measurement_id][key]['ip_addr']
            asn = self.measurement_dict[self.measurement_id][key]['asn']
            popup = ip_address
                
            ip = open(filename, 'a')

            # Create Green IP Address location Circles   
            ip.write(stringa + str(i)+stringb+str(lat)+ ','+str(lon)+string2+'\n')
            # Create Green circle Popup
            ip.write(string7a +str(i)+string7b+str(key) + string5 + 'AS '+str(asn)+"<br />" + str(ip_address) +string8)

            #print ("POPUP for ",lat," is ",popup[lat])




        #Create circle to denote AS
        ip.write(string7 +'asnumber'+string5+'owner'+string8)
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
        self.geolocator = Nominatim(user_agent="aswindow")
        #self.url_base = 'http://ipinfo.io/'
        #print ("this is the target "+ self.ip_name)
        self.create_html(self.target)
   

    

if __name__ == "__main__":
    os.chdir('/home/paul/Documents/ipgeoloc')
    IP = ''
    result = {}
    thistarget = target(IP)
    #print (thisas.get_company_info())
    #print (thisas.get_ipinfo())