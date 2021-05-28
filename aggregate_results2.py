# Tool to find the geo-cordinates of each target of a set of measurements and compare
# against the targets known geo-coordinates 

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

# Avg Speed of a packet in a fibre optic medium
packet_speed = 0.66 * 300000

# Format cell borders via a configurable RxC box
# 
def box(workbook, worksheet, first_row, first_col, rows_count, cols_count,thickness=1):
    if cols_count == 1 and rows_count == 1:
        # whole cell
        worksheet.conditional_format(first_row, first_col,
                                     first_row, first_col,
                                     {'type': 'formula', 'criteria': 'True',
                                     'format': workbook.add_format({'top': thickness, 'bottom':thickness,
                                                                    'left': thickness,'right':thickness})})    
    elif rows_count == 1:
        # left cap
        worksheet.conditional_format(first_row, first_col,
                                 first_row, first_col,
                                 {'type': 'formula', 'criteria': 'True',
                                  'format': workbook.add_format({'top': thickness, 'left': thickness,'bottom':thickness})})
        # top and bottom sides
        worksheet.conditional_format(first_row, first_col + 1,
                                 first_row, first_col + cols_count - 2,
                                 {'type': 'formula', 'criteria': 'True', 'format': workbook.add_format({'top': thickness,'bottom':thickness})})

        # right cap
        worksheet.conditional_format(first_row, first_col+ cols_count - 1,
                                 first_row, first_col+ cols_count - 1,
                                 {'type': 'formula', 'criteria': 'True',
                                  'format': workbook.add_format({'top': thickness, 'right': thickness,'bottom':thickness})})

    elif cols_count == 1:
        # top cap
        worksheet.conditional_format(first_row, first_col,
                                 first_row, first_col,
                                 {'type': 'formula', 'criteria': 'True',
                                  'format': workbook.add_format({'top': thickness, 'left': thickness,'right':thickness})})

        # left and right sides
        worksheet.conditional_format(first_row + 1,              first_col,
                                 first_row + rows_count - 2, first_col,
                                 {'type': 'formula', 'criteria': 'True', 'format': workbook.add_format({'left': thickness,'right':thickness})})

        # bottom cap
        worksheet.conditional_format(first_row + rows_count - 1, first_col,
                                 first_row + rows_count - 1, first_col,
                                 {'type': 'formula', 'criteria': 'True',
                                  'format': workbook.add_format({'bottom': thickness, 'left': thickness,'right':thickness})})

    else:
        # top left corner
        worksheet.conditional_format(first_row, first_col,
                                 first_row, first_col,
                                 {'type': 'formula', 'criteria': 'True',
                                  'format': workbook.add_format({'top': thickness, 'left': thickness})})

        # top right corner
        worksheet.conditional_format(first_row, first_col + cols_count - 1,
                                 first_row, first_col + cols_count - 1,
                                 {'type': 'formula', 'criteria': 'True',
                                  'format': workbook.add_format({'top': thickness, 'right': thickness})})

        # bottom left corner
        worksheet.conditional_format(first_row + rows_count - 1, first_col,
                                 first_row + rows_count - 1, first_col,
                                 {'type': 'formula', 'criteria': 'True',
                                  'format': workbook.add_format({'bottom': thickness, 'left': thickness})})

        # bottom right corner
        worksheet.conditional_format(first_row + rows_count - 1, first_col + cols_count - 1,
                                 first_row + rows_count - 1, first_col + cols_count - 1,
                                 {'type': 'formula', 'criteria': 'True',
                                  'format': workbook.add_format({'bottom': thickness, 'right': thickness})})

        # top
        worksheet.conditional_format(first_row, first_col + 1,
                                     first_row, first_col + cols_count - 2,
                                     {'type': 'formula', 'criteria': 'True', 'format': workbook.add_format({'top': thickness})})

        # left
        worksheet.conditional_format(first_row + 1,              first_col,
                                     first_row + rows_count - 2, first_col,
                                     {'type': 'formula', 'criteria': 'True', 'format': workbook.add_format({'left': thickness})})

        # bottom
        worksheet.conditional_format(first_row + rows_count - 1, first_col + 1,
                                     first_row + rows_count - 1, first_col + cols_count - 2,
                                     {'type': 'formula', 'criteria': 'True', 'format': workbook.add_format({'bottom': thickness})})

        # right
        worksheet.conditional_format(first_row + 1,              first_col + cols_count - 1,
                                     first_row + rows_count - 2, first_col + cols_count - 1,
                                     {'type': 'formula', 'criteria': 'True', 'format': workbook.add_format({'right': thickness})})

def get_measurements():
    # Get all measurement and probe IDs
    sql = "SELECT * FROM measurements"
    cursor.execute(sql,)
    m = cursor.fetchall()
    return m
def get_probe_info(probe):
    # Get IP geo Coordinates and addresss
    sql = "select * from probes where id  = %s"
    val = (probe,)
    cursor.execute(sql, val)
    p = cursor.fetchone()
    return p
def get_hops(measurement,probe):
    # Get all measurement and probe IDs
    sql = "SELECT * FROM hops where measurement = %s and probe = %s"
    val = (measurement, probe)
    cursor.execute(sql, val)
    h = cursor.fetchall()
    return h

def get_geo(ip_id):
    # Get IP geo Coordinates and addresss
    sql = "select * from geo where id  = %s"
    val = (ip_id,)
    cursor.execute(sql, val)
    i = cursor.fetchone()
    return i

def create_spreadsheet(spreadsheet_name):
    workbook = xlsxwriter.Workbook(spreadsheet_name+' .xlsx')
    worksheet = workbook.add_worksheet()

    # Add a bold format to use to highlight cells.
    bold = workbook.add_format({'bold': 1})
    worksheet.set_column(1, 1, 15)
    worksheet.write('A1', 'Source Probe', bold)
    
    return worksheet,workbook

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

    # Area under analysis
    area ='south_africa'
    # Ip addresses listed by IXPs in this area on PCH.net
    ixp_ips = ['196.223.14','196.223.30','196.10.140','196.223.22','196.10.141','196.60.8','196.60.9','196.60.10','196.60.11']
    # Additional Ip Addresses being used by IXP's
    ixp_unknown_ips = ['105.22.46',]

    # local subnets
    local_subnets = ['10.','172.16.','172.17.','172.18.','172.19.','172.20.','172.21.','172.22.',
    '172.23.','172.24.','172.25.','172.26.','172.27.','172.28.','172.29.','172.30.','172.31.','192.168.',
    '100.64.','100.65.','100.66.','100.67.','100.68.','100.69.',
    '100.70.','100.71.','100.72.','100.73.','100.74.','100.75.','100.76.','100.77.','100.78.',
    '100.79.','100.80.','100.81.','100.82.','100.83.','100.84.','100.85.','100.86.','100.87.',
    '100.88.','100.89.','100.90.','100.91.','100.92.','100.93.','100.94.','100.95.','100.96.',
    '100.97.','100.98.','100.99.','100.100.','100.101.','100.102.','100.103.','100.104.','100.105.',
    '100.106.','100.107.','100.108.','100.109.','100.110.','100.111.','100.112.','100.113.','100.114.',
    '100.115.','100.116.','100.117.','100.118.','100.119.','100.120.','100.121.','100.122.','100.123.',
    '100.124.','100.125.','100.126.','100.127.']

    # Create a spreadhseet which will store the best minimum times to each target
    overall_ws,overall_wb = create_spreadsheet('spreadsheets/'+area+'/min_measurements')
    bold_o = overall_wb.add_format({'bold': True})
    red_fill_o = overall_wb.add_format({'bg_color': 'red'})
    orange_fill_o = overall_wb.add_format({'bg_color': 'orange'})
    border_o = overall_wb.add_format({'bg_color': 'orange'})

    # get the measurements from the database
    measurements = get_measurements()

    # Create a list of Probes
    probe_list = []
    for measurement in measurements:
        probe_list.append(measurement[1])
    print(probe_list)
    # TEST OF JUST 1 measurement, remove this line to test all measurements 
    #measurements = [(28761866,1000492)]
    # Analyse each measurement
    measurement_dict = {}


    for measurement in measurements:
        this_measurement = measurement[0]
        this_target = measurement[1]
        measurement_dict[this_measurement] = {}
        # get all target probe information
        target_info = get_probe_info(this_target)
        print(target_info)
        if target_info == None:
            continue
        measurement_dict[this_measurement]['target_probe']      = target_info[0]
        measurement_dict[this_measurement]['target_lat']        = target_info[1]
        measurement_dict[this_measurement]['target_lon']        = target_info[2]
        measurement_dict[this_measurement]['target_asn']        = target_info[3]
        measurement_dict[this_measurement]['target_ip']         = target_info[4]
        measurement_dict[this_measurement]['target_isanchor']   = target_info[5]
        
        # Set up spreadsheet formats
        worksheet,workbook = create_spreadsheet('spreadsheets/'+area+'/target_'+measurement_dict[this_measurement]['target_ip'])
        
        bold = workbook.add_format({'bold': True})
        red_fill = workbook.add_format({'bg_color': 'red'})
        orange_fill = workbook.add_format({'bg_color': 'orange'})
        border = workbook.add_format({'bg_color': 'orange'})
        row = 0
        col = 0

        min_dist = 1000000
        max_col = 0

        # get all hops data for each source probe
        for source_probe in probe_list:
            row += 1
            col = 0
            # if source and target are same skip
            print("probe is ",source_probe)
            if source_probe == this_target :
                continue
            measurement_dict[this_measurement][source_probe] = {}
            source_info = get_probe_info(source_probe)
            print(source_info)
            measurement_dict[this_measurement][source_probe]['lat']        = source_info[1]
            measurement_dict[this_measurement][source_probe]['lon']        = source_info[2]
            measurement_dict[this_measurement][source_probe]['asn']        = source_info[3]
            measurement_dict[this_measurement][source_probe]['ip']         = source_info[4]
            measurement_dict[this_measurement][source_probe]['is_anchor']  = source_info[5]

            worksheet.write_string(row,col,str(source_probe))
            col += 1         
            hops = get_hops(this_measurement,source_probe)
            

            print(hops)
            if hops != []: 
                last_hop = int(len(hops))
                ixp_hop = 1
                first_hop =''
                from_ixp = False
                
                for h in range(last_hop):
                    hop = hops[h][3]
                    measurement_dict[this_measurement][source_probe][hop] ={}
                    
                    measurement_dict[this_measurement][source_probe][hop]['rtt']                                = hops[h][4]
                    measurement_dict[this_measurement][source_probe][hop]['hostname']                           = hops[h][5]
                    measurement_dict[this_measurement][source_probe][hop]['prefix']                             = hops[h][6]
                    measurement_dict[this_measurement][source_probe][hop]['ip']                                 = hops[h][7]
                    measurement_dict[this_measurement][source_probe][hop]['ip_id']                              = hops[h][8]
                    measurement_dict[this_measurement][source_probe][hop]['est_hop_distance_to_source']         = measurement_dict[this_measurement][source_probe][hop]['rtt'] /2 * packet_speed
                
                    worksheet.write(0,col,'hop'+str(hop)+' ip',bold)
                    
                    subnet = ''
                                     
                    if measurement_dict[this_measurement][source_probe][hop]['ip'] != None:
                        subnet = measurement_dict[this_measurement][source_probe][hop]['ip'].split('.')
                        subnet = subnet[0]+'.'+subnet[1]+'.'+subnet[2]
                        print('ip is ',measurement_dict[this_measurement][source_probe][hop]['ip'])
                        print("Subnet is",subnet)
                        if first_hop == '':
                            if not measurement_dict[this_measurement][source_probe][hop]['ip'].startswith(('100.64.','100.65.','100.66.','100.67.','100.68.','100.69.',
                            '100.70.','100.71.','100.72.','100.73.','100.74.','100.75.','100.76.','100.77.','100.78.',
                            '100.79.','100.80.','100.81.','100.82.','100.83.','100.84.','100.85.','100.86.','100.87.',
                            '100.88.','100.89.','100.90.','100.91.','100.92.','100.93.','100.94.','100.95.','100.96.',
                            '100.97.','100.98.','100.99.','100.100.','100.101.','100.102.','100.103.','100.104.','100.105.',
                            '100.106.','100.107.','100.108.','100.109.','100.110.','100.111.','100.112.','100.113.','100.114.',
                            '100.115.','100.116.','100.117.','100.118.','100.119.','100.120.','100.121.','100.122.','100.123.',
                            '100.124.','100.125.','100.126.','100.127.',
                            '10.','172.16.','172.17.','172.18.','172.19.','172.20.','172.21.','172.22.',
                            '172.23.','172.24.','172.25.','172.26.','172.27.','172.28.','172.29.','172.30.','172.31.','192.168.')):
                                first_hop = hop
                            

                        if measurement_dict[this_measurement][source_probe][hop]['ip'].startswith(('196.223.14','196.223.30','196.10.140','196.223.22','196.10.141','196.60.8','196.60.9','196.60.10','196.60.11','105.22.46')):  
                            worksheet.write(row,col,measurement_dict[this_measurement][source_probe][hop]['ip'],red_fill)
                            ixp_hop = hop
                        else:
                            worksheet.write(row,col,measurement_dict[this_measurement][source_probe][hop]['ip']  )
                    worksheet.set_column(col,col, 15)
                    col += 1
                    worksheet.write(0,col,'hop'+str(hop)+' rtt',bold)
                    worksheet.write(row,col,measurement_dict[this_measurement][source_probe][hop]['rtt']  )

                    #stt = float("{:.2f}".format(stt))
                    print("hop is",hop)
                    print(row, str(from_ixp))
                    print (measurement_dict[this_measurement][source_probe][hop])                                      
                    col += 1
                    if max_col < col:
                        max_col = col  
                
                if ixp_hop:
                    ixp_to_target_time = measurement_dict[this_measurement][source_probe][last_hop]['rtt'] - measurement_dict[this_measurement][source_probe][ixp_hop]['rtt'] 
                    ixp_to_target_distance = (ixp_to_target_time/2) * packet_speed
                else:
                    ixp_to_target_time = 1000000
                    ixp_to_target_distance = 1000000
                
                source_to_target_time = measurement_dict[this_measurement][source_probe][last_hop]['rtt']
                if source_to_target_time > 0:
                    source_to_target_distance = (source_to_target_time/2) * packet_speed
                else:
                    source_to_target_time = 1000000
                    source_to_target_distance = 1000000
                
                max_col = 100
                worksheet.write(0,max_col+1,'time to tgt from IXP',bold)
                worksheet.write(0,max_col+2,'dist to tgt from IXP',bold)
                worksheet.write(0,max_col+3,'time to tgt from source',bold)
                worksheet.write(0,max_col+4,'dist to tgt from source',bold)

                # Only write time and distance to target from IXP if an IXP was in the path
                if ixp_to_target_distance != 1000000:
                    worksheet.write(row,max_col+1, ixp_to_target_time , bold)
                    worksheet.set_column(max_col+1,max_col+1,15)
                    worksheet.write(row,max_col+2, ixp_to_target_distance, bold)
                    worksheet.set_column(max_col+2,max_col+2,15)
                    if min_dist > ixp_to_target_distance:
                        min_dist = ixp_to_target_distance
                        min_row  = row
                        from_ixp = True
                
                if min_dist > source_to_target_distance:
                    min_dist = source_to_target_distance
                    min_row  = row
                    from_ixp = False

                worksheet.write(row,max_col+3, source_to_target_time , bold)
                worksheet.set_column(max_col+3,max_col+1,15)
                worksheet.write(row,max_col+4, source_to_target_distance, bold)
                worksheet.set_column(max_col+4,max_col+2,15)
                
                
                
                
                if measurement_dict[this_measurement]['target_ip'] == '41.77.51.6':
                    print(min_row, str(from_ixp))
                    # input('a key')
                print('=============================================================================================================================')

                
                    
        worksheet.write(0,max_col+5,'Min dist to tgt',bold)
        worksheet.write(min_row,max_col+5, min_dist, bold)
        worksheet.set_column(max_col+5,max_col+5,15)  
        worksheet.write(0,max_col+6,'from_IXP',bold)
        worksheet.write(min_row,max_col+6, str(from_ixp), bold)
        worksheet.set_column(max_col+6,max_col+6,15)

        
        
        
        
        name = worksheet.get_name()

        print(name)
        box(workbook,worksheet,min_row,1,1,max_col+5)
        print()

              
        
        workbook.close()
        