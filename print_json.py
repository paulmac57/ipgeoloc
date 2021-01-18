import pprint
import os
import time
import collections
import sys
import xlsxwriter
from decimal import Decimal



class Html_Create:
    def __init__(self, probe_dict):
        #print(probe_dict)
        probe_list = list(probe_dict.keys())  
        print(probe_dict) 
        self.target_ip = probe_dict['target_ip']                 # gets destination address 
        self.target_lat = probe_dict['target_lat']
        self.target_lon = probe_dict['target_lon']
        self.target_address = probe_dict['target_address']






if __name__ == "__main__":
    import json 
    os.chdir('/home/paul/Documents/ipgeoloc')
    #open testfile
    with open("probes.json") as file:
        probes =json.load(file)
    html = Html_Create(probes)
    print (html.target_address, html.target_ip, html.target_lat, html.target_lon)

    workbook = xlsxwriter.Workbook('target_'+html.target_ip+' .xlsx')
    worksheet = workbook.add_worksheet()

    # Add a bold format to use to highlight cells.
    bold = workbook.add_format({'bold': 1})

 
    worksheet.set_column(1, 1, 15)

    # Write some data headers.
    worksheet.write('A1', 'Probe', bold)
    worksheet.write('B1', 'Tot STT', bold)
    worksheet.write('C1', 'Hop1 STT', bold)
    worksheet.write('D1', 'Hop1 Dist', bold)
    worksheet.write('E1', 'h1 Speed', bold)
    worksheet.write('F1', 'Hop2 STT', bold)
    worksheet.write('G1', 'Hop2 Dist', bold)
    worksheet.write('H1', 'h2 Speed', bold)
    worksheet.write('I1', 'Hop3 STT', bold)
    worksheet.write('J1', 'Hop3 Dist', bold)
    worksheet.write('K1', 'h3 Speed', bold)
    worksheet.write('L1', 'Hop4 STT', bold)
    worksheet.write('M1', 'Hop4 Dist', bold)
    worksheet.write('N1', 'h4 Speed', bold)
    worksheet.write('O1', 'Hop5 STT', bold)
    worksheet.write('P1', 'Hop5 Dist', bold)
    worksheet.write('Q1', 'h5 Speed', bold)
    worksheet.write('R1', 'STT', bold)
    worksheet.write('S1', 'Ping target', bold)

    
    # Start from the first cell below the headers.
    row = 1
    col = 0

    probe_list = list(probes.keys())
    pings = (0.722, 1.608, 1.7, 1.464, 0.525)
    count = 0 
    for probe in probe_list:
        if probe not in ( 'target_ip','target_address', 'target_lat', 'target_lon'):
            
            worksheet.write_string  (row, col,     probe)
            tot_stt = str(probes[probe]['total_rtt']/2)
            worksheet.write_string  (row, col + 1, tot_stt )
            for hop in range(probes[probe]['Hops']):
                #print('HERE',probes[probe][str(hop+1)])
                stt = probes[probe][str(hop+1)]['min_rtt']/2
                distance = probes[probe][str(hop+1)]['distance']
                hop_speed = ((float(distance)*1000)/stt)/300000

                stt = float("{:.2f}".format(stt))
                worksheet.write_string  (row, col + 2 + hop, str(stt))
                worksheet.write_string  (row, col + 3 + hop, str(distance))
                
                
                print ("Probe is ", probe,"hop is ", hop,"distance is ", distance, "stt is ", stt,"hop Speed is ",hop_speed)
                worksheet.write_string  (row, col + 4 + hop, str(hop_speed))
                col += 2
            stt = float("{:.2f}".format(stt))
            
            worksheet.write_string  (row, 17, str(stt))
            worksheet.write_string  (row, 18, str(pings[count]/2))
            
            count += 1
            row += 1
            col = 0

    
    workbook.close()

