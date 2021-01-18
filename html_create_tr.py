import pprint
import os
import time
import collections
import sys

from geopy.geocoders import Nominatim
import ipinfo

class Html_Create:
    def create_header_html(self, probe_dict):
        
        total_x = 0.0
        total_y = 0.0
        count = 0
        probe_list = list(probe_dict.keys())
        # Work out central latitude and longitude coordinates
        for probe in probe_list:
            count = count +1 
            
            total_x = total_x + float(probe_dict[probe]['probe_x'])
            total_y = total_y + float(probe_dict[probe]['probe_y'])
            
        
        
        central_lon = total_x / count                                   # central lat coordiantes
        central_lat = total_y / count                                   # central lon coordiantes

        # write default head info to new file
        
        cmd2 = 'chmod ' +'766 '+ self.filename
        cmd = 'cp html/head.html '+ self.filename
                
        os.system(cmd)
        # Fix File Permisssions
        os.system(cmd2)
                
        # Write latitude and longitude to html file for zoom location
        # open file 
        
        ip = open(self.filename, 'a')
        
        print(central_lat,central_lon)
        
        ip.write(str(central_lat)+", "+str(central_lon)+'], 12);\n')
        ip.close()
        

        # write tilelayer information to html file
        cmd = 'cat html/tilelayer.html >> '+ self.filename
        os.system(cmd)

        ###########################################################

    def create_probes(self,probe_id, probe_dict):

        asn             = probe_dict[probe_id]['probe_asn']
        ip_address      = probe_dict[probe_id]['probe_ip']
        lon             = probe_dict[probe_id]['probe_x']
        lat             = probe_dict[probe_id]['probe_y']
        hops            = probe_dict[probe_id]['Hops']

        group_name = "group" + probe_id
        ip = open(self.filename, 'a')
        

        # create ipaddress points on map in green circles
        stringa = "      var circle"
        stringb = " = L.circle(["
        string1 = "      // show the area of operation of the AS on the map\n      var polygon = L.polygon([\n"
        string2 = "], { color: 'red', fillColor: '#00', interactive: false, fillOpacity: 0.0, radius: "
        string21 = "], { color: 'red', fillColor: '#8000000', fillOpacity: 0.5, radius: "
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
        
        # show all landmarks on map
         
            
        ip = open(self.filename, 'a') 

        # Create Green Probe location - These are probes used in the calculation
        ip.write(stringa + str(probe_id)+stringb+str(lat)+ ','+str(lon)+string21+str(500)+string2a+'\n')  
        # Create Probe Popup
        ip.write(string7a +str(probe_id)+string7b+str(probe_id) + string5 + 'AS '+str(asn)+"<br />" + str(ip_address) + "<br />" + "Hops: "+str(hops) +string8a)

        # Create Feature group Layer and Checker

        ip.write("     var "+group_name+" = L.featureGroup();\n")
        #ip.write("     "+group_name+".bindPopup('"+group_name+"');\n")
        ip.write("     circle"+probe_id+".on('click', function(e) {if(map.hasLayer("+group_name+")){\n")
        ip.write("     map.removeLayer("+group_name+"); }\n")
        ip.write("     else {\n")
        ip.write("     map.addLayer("+group_name+"); };} )\n")

    def create_hop(self,probe_id,h,hop):

        group_name = "group" + probe_id

        stringa = "      var circle_"
        stringb = " = L.circle(["
        string22 = "], { color: 'blue', fillColor: '#8000000', fillOpacity: 0.5, radius: "
        string2a = " });"
        string5 = '</b><br />'
        string7a ='      circle_'
        string7b ='.bindPopup("<b>Probe '
        string8a = ' ");\n\n'

        ip = open(self.filename, 'a')
        # Create Blue hop location 
        name = str(probe_id)+'_' + h
        print('HOP',hop)
        ip.write(stringa + name +stringb+str(hop['hop_latitude'])+ ','+str(hop['hop_longitude'])+string22+str(500)+string2a+'\n')  
        # Create hop Popup
        ip.write(string7a +name+string7b+ name + string5 + 'AS '+hop['asn']+"<br />" + hop['from'] + "<br />" + "Address: "+hop['address']+string8a+"\n")

        # add to Featuregroup
        ip.write("     circle_" + name + ".addTo(" + group_name + ");\n")
            
    
    def create_lines_var(self,probe_id,h,current_lon,current_lat,new_lon,new_lat):
        group_name = "group" + probe_id
        name = str(probe_id)+'_' + h
        string1 = "      var latlng_"
        string1a = " = [ ["
        string2 = "],["
        string3 = "] ] ;"
        string4 = "      var pline_"
        string5 = " = L.polyline(latlng_"
        string6 = ", {color: 'red'});\n"
        ip = open(self.filename, 'a')
        #Create the line lat and lon variable
        ip.write(string1+name+string1a+str(current_lat)+', '+str(current_lon)+string2+str(new_lat)+', '+str(new_lon)+string3+'\n')
        # Create and add the line to the map
        ip.write(string4+name+string5+name+string6+'\n')

        # add to Featuregroup
        ip.write("     pline_"+name+".addTo("+group_name+");\n")

        

   

    def close_file(self):
        ip = open(self.filename, 'a')
        # Complete Script and write to file
        #ip.write(string7 +'asnumber'+string5+'owner'+string8)
        string9 = "    </script>\n  </body>\n</html>"
        ip.write (string9)
        ip.close()


        print (self.filename+ " Written Succesfully, copy it to your webserver")
        
    def __init__(self, probe_dict):
        #print(probe_dict)
        probe_list = list(probe_dict.keys())   
        target_ip = (probe_dict[probe_list[0]]['dest_address'])                 # gets destination address 
        
        self.filename = 'targets/target_tr_'+str(target_ip)+'.html'
        
        
        self.create_header_html(probe_dict)          # create the file (named after the target IP and centralise the map )
        
        #Create the Probes
        for probe_id in probe_list:
            self.create_probes(probe_id,probe_dict)  
            

            # Create The HOPs
            print(probe_dict[probe_id].keys())
            current_lon = probe_dict[probe_id]['probe_x']
            current_lat = probe_dict[probe_id]['probe_y']
            hops =  int(probe_dict[probe_id]['Hops'])
            print("HOPS ARE",hops)
            
            for hop in range(hops):
                print(hop)
                h = str(hop+1)
                print(h)
                print(probe_dict[probe_id][h])
                self.create_hop(probe_id,h,probe_dict[probe_id][h])
                #CREATE the LINE BETWEEN the Hops
                new_lon = probe_dict[probe_id][h]['hop_longitude']
                new_lat = probe_dict[probe_id][h]['hop_latitude']    
                self.create_lines_var(probe_id,h,current_lon,current_lat,new_lon,new_lat)
                current_lat = new_lat
                current_lon = new_lon
            

        #CREATE TARGET

        self.close_file() 

        
        '''


        #self.target = probe_dict[0]['dest_address']
               
        #print ("this is the target "+ self.target)
        #self.create_html(self.target)
        '''
if __name__ == "__main__":
    import json 
    os.chdir('/home/paul/Documents/ipgeoloc')
    #open testfile
    with open("probes.json") as file:
        probes =json.load(file)
    html = Html_Create(probes)
