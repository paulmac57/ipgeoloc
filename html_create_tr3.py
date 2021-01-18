import pprint
import os
import time
import collections
import sys

from geopy.geocoders import Nominatim
import ipinfo
from decimal import Decimal

class Html_Create:
    def create_header_html(self, probe_dict):
        
        total_x = 0.0
        total_y = 0.0
        count = 0
        probe_list = list(probe_dict.keys())
        # Work out central latitude and longitude coordinates
        for probe in probe_list:
            if probe not in ('target_ip','target_address', 'target_lat', 'target_lon'):
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
        target_name = "target_" + probe_id
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

        ip.write ('      // Probe '+probe_id+'\n')

        # Create Green Probe location - These are probes used in the calculation
        ip.write(stringa + str(probe_id)+stringb+str(lat)+ ','+str(lon)+string21+str(500)+string2a+'\n')  
        # Create Probe Popup
        ip.write(string7a +str(probe_id)+string7b+str(probe_id) + string5 + 'AS '+str(asn)+"<br />" + str(ip_address) + "<br />" + "Hops: "+str(hops) +string8a)

        # Create Feature group Layer and Checker

        ip.write("      var "+group_name+" = L.featureGroup();\n")
        #ip.write("     "+group_name+".bindPopup('"+group_name+"');\n")
        ip.write("      circle"+probe_id+".on('click', function(e) {if(map.hasLayer("+group_name+")){\n")
        ip.write("        map.removeLayer("+group_name+"); ")
        ip.write("        map.removeLayer("+target_name+"); }\n")
        ip.write("      else {\n")
        ip.write("        map.addLayer("+group_name+"); };} )\n")

    def create_hop(self,probe_id,h,hop,rtt):

        group_name = "group" + probe_id
        target_name = "target_" + probe_id

        stringa = "      var circle_"
        stringb = " = L.circle(["
        string22 = "], { color: 'blue', fillColor: '#8000000', fillOpacity: 0.5, radius: "
        string2a = " });"
        string5 = '</b><br />'
        string7a ='      circle_'
        string7b ='.bindPopup("<b>Hop '
        string8a = ' ");\n\n'

        ip = open(self.filename, 'a')
        # Create Blue hop location 
        name = str(probe_id)+'_' + h
        print('HOP',hop)
        ip.write ('      // Probe '+probe_id+ ' Hop '+h+'\n')
        ip.write(stringa + name +stringb+str(hop['hop_latitude'])+ ','+str(hop['hop_longitude'])+string22+str(300)+string2a+'\n')  
        # Create hop Popup
        ip.write(string7a +name+string7b+ name + string5 + 'AS '+hop['asn']+"<br />" + str(hop['from']) + "<br />" + "Address: "+hop['address']+ "<br />" + "stt : " + str(rtt/2)+string8a+"\n")   
        # add to Featuregroup
        ip.write("      circle_" + name + ".addTo(" + group_name +");\n")
       
    def create_target(self,probe_id,h,hop,rtt):

        group_name = "group" + probe_id
        target_name = "target_" + probe_id
        name = str(probe_id)+'_' + h

        stringa = "      var circle_"
        stringb = " = L.circle(["
        stringt = "      var target_"
        string22 = "], { color: 'yellow', fillColor: 'yellow', fillOpacity: 0.5, radius: "
        string22t = "], { color: 'yellow', fillColor: '#8000000', fillOpacity: 0.5, radius: "
        string2a = " });"
        string5 = '</b><br />'
        string7a ='      circle_'
        string7t ='      target_'
        string7b ='.bindPopup("<b>Target '
        string8a = ' ");\n\n'

        ip = open(self.filename, 'a')

        # Create Yellow target location 
        name = str(probe_id)+'_' + h
        print('HOP',hop)
        ip.write ('      // Create target for Probe '+probe_id+ '\n')
        ip.write(stringa + name +stringb+str(hop['hop_latitude'])+ ','+str(hop['hop_longitude'])+string22+str(100)+string2a+'\n')  
        # Create target Popup
        ip.write(string7a +name+string7b+ name + string5 + 'AS '+hop['asn']+"<br />" + str(hop['from']) + "<br />" + "Address: "+hop['address']+ "<br />" + "stt : " + str(rtt/2)+string8a+"\n")   
        # add to Featuregroup
        ip.write("      circle_" + name + ".addTo(" + group_name +");\n")

        ip.write('      //___________________________________________\n')

        # Create target group and check if hop is clicked
        ip.write("      // Create target group and check if target is clicked\n")
        ip.write("      var "+target_name+" = L.featureGroup();\n")
        ip.write("      circle_"+probe_id +'_' + h+".on('click', function(e) {if(map.hasLayer("+target_name+")){\n")
        ip.write("        map.removeLayer("+target_name+"); }\n")
        ip.write("      else {\n")
        ip.write("        map.addLayer(" + target_name + ");\n")
        ip.write("        target_" + name + ".bringToBack();  };} )\n")
        ip.write('      //___________________________________________\n')
        # Create Yellow Target Area
        
        #  
        name = str(probe_id)+'_' + h
        
        print('HOP',hop)
        speed = .6 * 300000 # Average Speed of a packet in a Fibre medium
        r = rtt/2 * speed    # radius of target area in Metres  
        radius = int(r)
        print("radius is "+ str(radius))
        ip.write ('      // Create target area for Probe '+probe_id+ '\n')
        ip.write(stringt + name +stringb+str(hop['hop_latitude'])+ ','+str(hop['hop_longitude'])+string22t+str(radius)+string2a+'\n')  
        # Create target area Popup
        ip.write(string7t +name+string7b+ name + string5 + 'AS '+hop['asn']+"<br />" + hop['from'] + "<br />" + "Address: "+hop['address']+ "<br />" + "Estimated Local network Speed : .6C"+"<br />" + "Target Radius : " + str(radius/1000) +" Km"+string8a+"\n")

        # add to Featuregroup
        ip.write(string7t + name + ".addTo(" + target_name + ");\n")

                
        
    
            
    

    
        


    def create_lines_var(self,probe_id,h,current_lon,current_lat,new_lon,new_lat,distance,rtt,current_ip,new_ip):
        group_name = "group" + probe_id
        name = str(probe_id)+'_' + h
        string1 = "      var latlng_"
        string1a = " = [ ["
        string2 = "],["
        string3 = "] ] ;"
        string4 = "      var pline_"
        string5 = " = L.polyline(latlng_"
        string6 = ", {color: '"
        string6a = "'});\n"

        string7a ='        pline_'
        string7b ='.bindPopup("<b>Hop '
        string7c = '</b><br />'
        string8a = ' ");\n\n'
        ip = open(self.filename, 'a')
        
        # Work out speed of link (ie Congestion plus Packet processing overhead)
        # Average Speed of packet though fibre cable 2/3C  = 200 km per millisecond
        average_speed_fraction = .66          # Average speed of a packet in optical fibre
        packet_speed = (distance*1000) / (rtt/2)         # speed of packet in km per sec
        sol_fraction = packet_speed/ 300000   # Compared against speed of light

        if sol_fraction < .2:
            colour = "red"
        if sol_fraction >= .2 and sol_fraction < .3:
            colour = "orange"
        if sol_fraction >= .3 and sol_fraction < .5:
            colour = "yellow"
        if sol_fraction >= .5:
            colour = "green"
        
        ip.write ('      // Probe '+probe_id+ ' Line '+h+'\n')
        #Create the line lat and lon variable
        ip.write(string1+name+string1a+str(current_lat)+', '+str(current_lon)+string2+str(new_lat)+', '+str(new_lon)+string3+'\n')
        # Create and add the line to the map
        ip.write(string4+name+string5+name+string6+colour+string6a+'\n')
        # Create Line Popup
        ip.write("      pline_"+name+string7b+ name + string7c + 'From: ' + str(current_ip)+ ' To: '+str(new_ip)+"<br />"'Distance: '+ str(distance)+" Km<br />" + "Stt: "+str(rtt/2)  + "<br />" +"Average Speed of packet in fibre: .66 Speed of light"+"<br />"+"Packet Speed Over This Hop: " +str(sol_fraction)  +string8a+"\n")
        
        # add to Featuregroup
        ip.write("      pline_"+name+".addTo("+group_name+");\n")

    def probe_check_dup_coords(self,probe_id,probe_dict):   

        probe_list = list(probe_dict.keys())
        # Work out if coordinates are already in use.

        lon             = probe_dict[probe_id]['probe_x']
        lat             = probe_dict[probe_id]['probe_y']
        for probe in probe_list:
            # if they are adjust the circle a small amount so that it displays
            # TODO need to include a note that this has been done in popup
            if probe not in ( probe_id, 'target_ip','target_address', 'target_lat', 'target_lon'):
                if lon == probe_dict[probe]['probe_x']:
                    if lat == probe_dict[probe]['probe_y']:
                        probe_dict[probe]['probe_x'] = lon + .0010
                        probe_dict[probe]['probe_y'] = lat - .0010
            
                
   

    def close_file(self):
        ip = open(self.filename, 'a')
        # Complete Script and write to file
        #ip.write(string7 +'asnumber'+string5+'owner'+string8)
        string9 = "    </script>\n  </body>\n</html>"
        ip.write (string9)
        ip.close()


        print (self.filename+ " Written Succesfully, copy it to your webserver")
        
    def __init__(self, probe_dict):
        print(probe_dict)
        probe_list = list(probe_dict.keys())  
        print (probe_list)
        print(probe_dict['target_ip']) 
                        # gets destination address 
        self.target_ip = str(probe_dict['target_ip'])                # gets destination address 
        self.target_lat = probe_dict['target_lat']
        self.target_lon = probe_dict['target_lon']
        self.target_address = probe_dict['target_address']

       
        self.filename = 'targets/target_tr_'+str(self.target_ip)+'.html'
        
        
        self.create_header_html(probe_dict)          # create the file (named after the target IP and centralise the map )
        
        #Create the Probes
        for probe_id in probe_list:
            # Only iterate through probe ID's not other information
            if probe_id not in ('target_ip','target_address', 'target_lat', 'target_lon'):
                # check if 2 probes have same Coordinates and slightly change the
                # coordinates of one To ensure both probes display on map
                self.probe_check_dup_coords(probe_id,probe_dict)
                # Now create the probes 
                self.create_probes(probe_id,probe_dict)  
                # Create The HOPs
                current_lon = probe_dict[probe_id]['probe_x']
                current_lat = probe_dict[probe_id]['probe_y']
                current_rtt = 0
                if probe_dict[probe_id]['probe_ip'] != None:
                    current_ip = probe_dict[probe_id]['probe_ip']
                else:
                    current_ip = 'unknown'
                hops =  int(probe_dict[probe_id]['Hops'])
                
                for hop in range(hops):
                    print(hop)
                    h = str(hop+1)
                    print(h)
                    print(probe_dict[probe_id][h])
                    #CREATE the LINE BETWEEN the Hops
                    new_lon = probe_dict[probe_id][h]['hop_longitude']
                    new_lat = probe_dict[probe_id][h]['hop_latitude'] 
                    distance = probe_dict[probe_id][h]['distance']                    
                    new_ip = probe_dict[probe_id][h]['from'] 
                    new_rtt = probe_dict[probe_id][h]['min_rtt'] 
                    
                    # would have been great if RTT increase at each hop, however 
                    # routers can change priority of packet causing chaos with this method
                    rtt_diff = new_rtt - current_rtt 
                    rtt = new_rtt
                    print(current_ip,new_ip)
                    self.create_lines_var(probe_id,h,current_lon,current_lat,new_lon,new_lat,distance,rtt,current_ip,new_ip)
                    current_lat = new_lat
                    current_lon = new_lon
                    current_ip = new_ip
                    current_rtt = new_rtt
                    # if this is the target (ie final hop) then show it as a yellow target
                    if probe_dict[probe_id][h]['from'] == probe_dict[probe_id]['dest_address']:
                        print("********************************")
                        # Testing to see if using the difference between the second last hop and last hop helps witha accuracy.
                        self.create_target(probe_id,h,probe_dict[probe_id][h],rtt_diff)
                    else:
                        # Create a blue hop
                        self.create_hop(probe_id,h,probe_dict[probe_id][h],rtt)
                    


                # Create a greater circle from final hop to show target area 
                # THIS MAY NEED CHECKING IF THE DISTANCE ON THE FINAL HOP IS GREATER THAN 0
                # This sets a target area around the last hop
                #self.create_target_error_circle(probe_id,h,probe_dict[probe_id][h],probe_dict[probe_list[0]])

            #CREATE TARGET

            # Create Actual Target location - This is for comparison only
            #ip.write(stringa + str(i+3)+stringb+str(target_latitude)+ ','+str(target_longitude)+string25+str(250)+string2a+'\n') 
            #ip.write(string7a +str(i+3)+string7c+ str(target_ip) +"<br />" + str(target_address) +string8a)


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
