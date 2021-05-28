# created to check all IP addresses that have NULL coords

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
# USing chargeable Google if nominatum fails to find hop coordiantes https://pypi.org/project/geocoder/
import geocoder
k = 'AIzaSyD19RPrdUrUp0Vlei08vSCpcUBR3FQoxqY'



def get_coords(address):            
    g = geocoder.google(address, key = k)
    if g != None:
        x = g.lng
        y = g.lat 
    else:
        x = 0
        y = 0                           
                    
            
    return x,y





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
    

    

    # Get all ip's with null lats
    sql = "SELECT * FROM geo WHERE lat is NULL"
    
    cursor.execute(sql)
    m = cursor.fetchall()
    #print("ip info is", m)
    for line in m:
        address = line[4]
        id = line[0]
        if address != "local":
        
            x,y = get_coords(address)
            

            sql = "Update geo set lat = %s, lon = %s where id = %s "
            val = (y,x,id)
            print (id, y,x, address)
            cursor.execute(sql,val)
            
            mydb.commit()
         
    
    
    '''
    # get all hops from all probes for this measurement
    sql = "select * from hops where measurement = %s"
    val = (m)
    cursor.execute(sql, val)
    hops = cursor.fetchall()

    print (m)
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
