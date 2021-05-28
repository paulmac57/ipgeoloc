import pprint
import os
import time
import collections
import sys
import xlsxwriter
import mysql.connector
import csv
import json
from decimal import Decimal
from geopy.distance import geodesic



if __name__ == "__main__":
    import json 
    os.chdir('/home/paul/Documents/ipgeoloc')
    #open testfile
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="brindle7",
    database="ipgeo"
    )
    cursor = mydb.cursor()

    target_probe = 1000492

    # Get Target Probes Coordinates
    sql = "SELECT * FROM probes WHERE id = %s"
    val = (target_probe,)
    cursor.execute(sql, val)
    p = cursor.fetchone()
    print("Probe info is", p)
    target_lat = p[1]
    target_lon = p[2]
    target_ip = p[4]
    target_isanchor = p[5]
    target_coords = (target_lat, target_lon)


    # Get measurement where above is the target probe
    sql = "SELECT id FROM measurements WHERE target_id = %s"
    val = (target_probe,)
    cursor.execute(sql, val)
    m = cursor.fetchone()
    print("measurement is", m)

    # get all hops from all probes for this measurement
    sql = "select * from hops where measurement = %s"
    val = (m)
    cursor.execute(sql, val)
    hops = cursor.fetchall()

    #print (m)
    # Create a dictionary of probes and hops
    probe_dict = {}
    last_probe = 0

    for id in hops:
        #
        # print(id)
        probe = id[2]
        hop = id[3]
        rtt =id[4]
        hostname = id[5]
        prefix =id[6]
        ip= id[7]
        ip_id = id[8]
        if probe != last_probe:
            probe_dict[probe] = {}
        probe_dict[probe]['max_hops'] = hop
        probe_dict[probe][hop] = {}
        probe_dict[probe][hop]['rtt'] = rtt
        probe_dict[probe][hop]['hostname'] = hostname
        probe_dict[probe][hop]['prefix'] = prefix 
        probe_dict[probe][hop]['ip'] = ip
        probe_dict[probe][hop]['ip_id'] = ip_id 
        
        last_probe = probe
        
        #print(probe,hop,probe_dict[probe][hop])
    final_hop_ip_id_list = []
    final_hop_dict = {}
    smallest_hop  = 100
    
    # Find ip address ID and RTT value of final hop of each probe

    for probe in probe_dict:
        
        #print(probe, probe_dict[probe])
        if probe == target_probe:
            continue
        print (probe)
        final_hop =  probe_dict[probe]['max_hops']    
        pen_hop = final_hop-1 
        if pen_hop == 0:
            pen_hop =1
        print ('Pen hop is ',pen_hop)  
        final_hop_rtt = probe_dict[probe][final_hop]['rtt']
        penultimate_hop_rtt = probe_dict[probe][pen_hop]['rtt']

        if final_hop_rtt < smallest_hop:
            smallest_hop = final_hop_rtt
            previous_hop = penultimate_hop_rtt
            smallest_probe = probe
        final_hop_ip = probe_dict[probe][final_hop]['ip']
        final_hop_ip_id = probe_dict[probe][final_hop]['ip_id']
        if final_hop_ip_id != None and final_hop_ip_id not in final_hop_dict:
            final_hop_dict[final_hop_ip_id] ={}
        
        if final_hop_ip_id != None:
            final_hop_dict[final_hop_ip_id]['smallest_hop'] = smallest_hop
            final_hop_dict[final_hop_ip_id]['probe'] = smallest_probe
            final_hop_dict[final_hop_ip_id]['penultimate_hop'] = previous_hop


        

                  
        print(final_hop_dict)

    # Work out distances from final hops
    


    for id in final_hop_dict:
        
        # Get location info of last hop ip
        sql = "SELECT ip,lat,lon,address FROM geo WHERE id = %s"
        val = (id,)
        cursor.execute(sql, val)
        ip_coords_info = cursor.fetchone()
        
        ip = ip_coords_info[0]
        lat = ip_coords_info[1]
        lon = ip_coords_info[2]
        address = ip_coords_info[3]

        final_rtt = final_hop_dict[id]['smallest_hop']
        penultimate_rtt = final_hop_dict[id]['penultimate_hop']
        source_probe = final_hop_dict[id]['probe']
         
        
        
        print("this is the source probe",source_probe)
        
        #what is the location of the source probe
        sql = "SELECT * FROM probes WHERE id = %s"
        val = (source_probe,)
        cursor.execute(sql, val)
        p = cursor.fetchone()
        print("Source Probe info is", p)
        lat_source = p[1]
        lon_source = p[2]
        asn_source = p[3]
        ip_source = p[4]
        isanchor_source = p[5]

        source_coords = (lat_source,lon_source)


        
        rtt_distance = (final_rtt/2) * ((.66*300000)/1000)
        penultimate_distance = ((final_rtt-penultimate_rtt)/2) * ((.66*300000)/1000)
        print(ip,rtt_distance,'(km)',lat,lon,address)

        last_hop_coords = (lat,lon)

       


        # work out Actual(approximated if using probe, Real if using Anchor) distance from last hop to target

        distance = geodesic(source_coords, target_coords)
        
        print ('Actual distance is from source probe',source_probe,' to target probe',target_probe ,'is ',distance)
        print ('Distance according to RTT values is within a',rtt_distance, 'km radius of the source probe,',source_probe,'at',last_hop_coords)
        print ( ' Distance worked out by using final hop RTT - penultimate hop RTT is ',penultimate_distance)
    '''
    
    # Get all measurements where the target probe is now the Source probe
    sql = "SELECT id FROM measurements"
    val = (target_probe,)
    cursor.execute(sql, val)
    measurements = cursor.fetchall()
    print("measurement is", measurements)

    for m in measurements:
        # get all hops from all probes for this measurement
        sql = "select * from hops where probe = %s"
        val = (m)
        cursor.execute(sql, val)
        hops = cursor.fetchall()







        

    # get id, coords, ip, isanchor  of source probe
    
    # get rtt, hostname. prefix, ip, ip_id of first hop where id = probe  (is source probe )

    # use ip_id to get coords of hop to get coords of hop

    # work out distance from x1,y1 to x2,y2 also work out distance via rtt time * .66 * 300000

    # repeat to last hop

    # Plot location of target probe using infor pprovided bt RIPE ATLAS = Result1

    # Create greater circle from last hop using rtt of last hop = REsult2

    # compare rtt vs actual

    # do a ripe ipmap check also and plot that = Result3

    # are there any diffetnt last hops, can we use multilateration to reduce the error radius ? = Result4


     
    # get  
  




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
    worksheet.write('A1', 'Source Probe', bold)
    worksheet.write('B1', 'Tot RTT', bold)
    worksheet.write('C1', 'Hop1 RTT', bold)
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
    '''
