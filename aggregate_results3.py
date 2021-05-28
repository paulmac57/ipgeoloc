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
import sqlite3
import numpy as np
from scipy.optimize import brentq
from decimal import Decimal
from geopy.distance import geodesic

# Avg Speed of a packet in a fibre optic medium
packet_speed = 0.66 * 300000

# Default database in same folder as this script
DEFAULT_DB_PATH = os.path.join(os.path.dirname(__file__), 'peeringdb.sqlite3')

# Connection to Peeringdb locally Synced database
def db_connect(db_path=DEFAULT_DB_PATH):
    con = sqlite3.connect(db_path)
    return con

# Format cell borders via a configurable RxC box
#


def box(workbook, worksheet, first_row, first_col, rows_count, cols_count, thickness=1):
    if cols_count == 1 and rows_count == 1:
        # whole cell
        worksheet.conditional_format(first_row, first_col,
                                     first_row, first_col,
                                     {'type': 'formula', 'criteria': 'True',
                                     'format': workbook.add_format({'top': thickness, 'bottom': thickness,
                                                                    'left': thickness, 'right': thickness})})
    elif rows_count == 1:
        # left cap
        worksheet.conditional_format(first_row, first_col,
                                 first_row, first_col,
                                 {'type': 'formula', 'criteria': 'True',
                                  'format': workbook.add_format({'top': thickness, 'left': thickness, 'bottom': thickness})})
        # top and bottom sides
        worksheet.conditional_format(first_row, first_col + 1,
                                 first_row, first_col + cols_count - 2,
                                 {'type': 'formula', 'criteria': 'True', 'format': workbook.add_format({'top': thickness, 'bottom': thickness})})

        # right cap
        worksheet.conditional_format(first_row, first_col + cols_count - 1,
                                 first_row, first_col + cols_count - 1,
                                 {'type': 'formula', 'criteria': 'True',
                                  'format': workbook.add_format({'top': thickness, 'right': thickness, 'bottom': thickness})})

    elif cols_count == 1:
        # top cap
        worksheet.conditional_format(first_row, first_col,
                                 first_row, first_col,
                                 {'type': 'formula', 'criteria': 'True',
                                  'format': workbook.add_format({'top': thickness, 'left': thickness, 'right': thickness})})

        # left and right sides
        worksheet.conditional_format(first_row + 1,              first_col,
                                 first_row + rows_count - 2, first_col,
                                 {'type': 'formula', 'criteria': 'True', 'format': workbook.add_format({'left': thickness, 'right': thickness})})

        # bottom cap
        worksheet.conditional_format(first_row + rows_count - 1, first_col,
                                 first_row + rows_count - 1, first_col,
                                 {'type': 'formula', 'criteria': 'True',
                                  'format': workbook.add_format({'bottom': thickness, 'left': thickness, 'right': thickness})})

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


def orange(workbook, worksheet, row, col):
    worksheet.conditional_format(row, col,
                                     row, col,
                                     {'type': 'formula', 'criteria': 'True',
                                     'format': workbook.add_format({'bg_color': 'orange'})})


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


def get_hops(measurement, probe):
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

    return worksheet, workbook

# check distance between last location and current location


def check_distance(c_x, c_y, h_x, h_y):

    coords_1 = (c_y, c_x)
    coords_2 = (h_y, h_x)
    distance = geodesic(coords_1, coords_2).meters
    return distance


# TODO Intersection area is not currently used 
def intersection_area(d, R, r):
    """Return the area of intersection of two circles.

    The circles have radii R and r, and their centres are separated by d.

    """

    if d <= abs(R-r):
        # One circle is entirely enclosed in the other.
        return np.pi * min(R, r)**2
    if d >= r + R:
        # The circles don't overlap at all.
        return 0

    r2, R2, d2 = r**2, R**2, d**2
    alpha = np.arccos((d2 + r2 - R2) / (2*d*r))
    beta = np.arccos((d2 + R2 - r2) / (2*d*R))
    return ( r2 * alpha + R2 * beta -
             0.5 * (r2 * np.sin(2*alpha) + R2 * np.sin(2*beta))
           )
# TODO Intersection area is not currently used 
def find_d(A, R, r):
    """
    Find the distance between the centres of two circles giving overlap area A.

    """

    # A cannot be larger than the area of the smallest circle!
    if A > np.pi * min(r, R)**2:
        raise ValueError("Intersection area can't be larger than the area"
                         " of the smallest circle")
    if A == 0:
        # If the circles don't overlap, place them next to each other
        return R+r

    if A < 0:
        raise ValueError('Negative intersection area')

    def f(d, A, R, r):
        return intersection_area(d, R, r) - A

    a, b = abs(R-r), R+r
    d = brentq(f, a, b, args=(A, R, r))
    return d

if __name__ == "__main__":
    import json
    os.chdir('/home/paul/Documents/ipgeoloc')
    # open testfile
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="brindle7",
    database="ipgeo"
    )
    cursor = mydb.cursor()

    # Area under analysis
    area = 'south_africa'

    # Ip addresses listed by IXPs in this area on PCH.net
    ixp_ips = ['196.223.14', '196.223.30', '196.10.140', '196.223.22',
        '196.10.141', '196.60.8', '196.60.9', '196.60.10', '196.60.11']
    # Additional Ip Addresses being used by IXP's
    ixp_unknown_ips = ['105.22.46', ]

    # local subnets
    local_subnets = ['10.', '172.16.', '172.17.', '172.18.', '172.19.', '172.20.', '172.21.', '172.22.',
    '172.23.', '172.24.', '172.25.', '172.26.', '172.27.', '172.28.', '172.29.', '172.30.', '172.31.', '192.168.',
    '100.64.', '100.65.', '100.66.', '100.67.', '100.68.', '100.69.',
    '100.70.', '100.71.', '100.72.', '100.73.', '100.74.', '100.75.', '100.76.', '100.77.', '100.78.',
    '100.79.', '100.80.', '100.81.', '100.82.', '100.83.', '100.84.', '100.85.', '100.86.', '100.87.',
    '100.88.', '100.89.', '100.90.', '100.91.', '100.92.', '100.93.', '100.94.', '100.95.', '100.96.',
    '100.97.', '100.98.', '100.99.', '100.100.', '100.101.', '100.102.', '100.103.', '100.104.', '100.105.',
    '100.106.', '100.107.', '100.108.', '100.109.', '100.110.', '100.111.', '100.112.', '100.113.', '100.114.',
    '100.115.', '100.116.', '100.117.', '100.118.', '100.119.', '100.120.', '100.121.', '100.122.', '100.123.',
    '100.124.', '100.125.', '100.126.', '100.127.']

    # Create a spreadhseet which will store the best minimum times to each target
    overall_ws, overall_wb = create_spreadsheet(
        'spreadsheets/'+area+'/min_measurements')
    bold_o = overall_wb.add_format({'bold': True})
    red_fill_o = overall_wb.add_format({'bg_color': 'red'})
    orange_fill_o = overall_wb.add_format({'bg_color': 'orange'})
    border_o = overall_wb.add_format({'bg_color': 'orange'})

    overall_ws.write(0, 0, 'target_ip', bold_o)
    overall_ws.write(0, 1, 'target_id', bold_o)
    overall_ws.write(0, 2, 'target_lat', bold_o)
    overall_ws.write(0, 3, 'target_lon', bold_o)

    overall_ws.write(0, 4, 't_to_lr_time', bold_o)
    overall_ws.write(0, 5, 't_to_lr_ixp_ip', bold_o)
    overall_ws.write(0, 6, 't_to_lr_ixp_lat', bold_o)
    overall_ws.write(0, 7, 't_to_lr_ixp_lon', bold_o)
    overall_ws.write(0, 8, 't_to_lr_lr_ip', bold_o)

    overall_ws.write(0, 9, 's_to_t_time', bold_o)
    overall_ws.write(0, 10, 's_to_t_s_ip', bold_o)
    overall_ws.write(0, 11, 's_to_t_s_id', bold_o)
    overall_ws.write(0, 12, 's_to_t_s_lat', bold_o)
    overall_ws.write(0, 13, 's_to_t_s_lon', bold_o)
    overall_ws.write(0, 14, 's_to_t_ixp_ip', bold_o)
    overall_ws.write(0, 15, 's_to_t_ixp_lat', bold_o)
    overall_ws.write(0, 16, 's_to_t_ixp_lon', bold_o)
    overall_ws.write(0, 17, 's_to_t_lr_ip', bold_o)

    overall_ws.write(0, 18, 's_to_lr_time', bold_o)
    overall_ws.write(0, 19, 's_to_lr_s_ip', bold_o)
    overall_ws.write(0, 20, 's_to_lr_s_id', bold_o)
    overall_ws.write(0, 21, 's_to_lr_s_lat', bold_o)
    overall_ws.write(0, 22, 's_to_lr_s_lon', bold_o)
    overall_ws.write(0, 23, 's_to_lr_ixp_ip', bold_o)
    overall_ws.write(0, 24, 's_to_lr_ixp_lat', bold_o)
    overall_ws.write(0, 25, 's_to_lr_ixp_lon', bold_o)
    overall_ws.write(0, 26, 's_to_lr_lr_ip', bold_o)

    overall_ws.write(0, 27, 'i_to_lr_time', bold_o)
    overall_ws.write(0, 28, 'i_to_lr_ixp_ip', bold_o)
    overall_ws.write(0, 29, 'i_to_lr_ixp_lat', bold_o)
    overall_ws.write(0, 30, 'i_to_lr_ixp_lon', bold_o)
    overall_ws.write(0, 31, 'i_to_lr_lr_ip', bold_o)

    overall_ws.write(0, 32, 'i_to_t_time', bold_o)
    overall_ws.write(0, 33, 'i_to_t_ixp_ip', bold_o)
    overall_ws.write(0, 34, 'i_to_t_ixp_lat', bold_o)
    overall_ws.write(0, 35, 'i_to_t_ixp_lon', bold_o)
    overall_ws.write(0, 36, 'i_to_t_lr_ip', bold_o)

    overall_ws.write(0, 37, 'il_distance', bold_o)
    overall_ws.write(0, 38, 'tl_distance', bold_o)
    overall_ws.write(0, 39, 'sl_distance', bold_o)

    overall_ws.write(0, 40, 'Act_it_distance', bold_o)
    overall_ws.write(0, 41, 'Act_st_distance', bold_o)

    overall_ws.set_column(0, 41, 15)

    # Create a web based menu to provide easy access to Target maps
    menu_file = 'targets/southafrica/menu.html'
    cmd = 'rm ' + menu_file
    os.system(cmd)
    menu = open(menu_file,'a')
    # Fix File Permisssions
    menu.write('<!DOCTYPE html>\n<html>\n<body>\n\n<h1>South Africa target Links</h1>\n')
    

    # get the measurements from the measurements database
    measurements = get_measurements()

    # Create a list of Probes
    probe_list = []
    for measurement in measurements:
        probe_list.append(measurement[1])
    print(probe_list)
    # TEST OF JUST 1 measurement, remove this line to test all measurements
    #measurements = [(28761866,1000492)]
    #measurements = [(28761863,1000237)]
    
    # Analyse each measurement
    measurement_dict = {}
    o_row = 0

    results_dict = {}

    for measurement in measurements:
        this_measurement = measurement[0]
        this_target = measurement[1]
        measurement_dict[this_measurement] = {}
        # get all target probe information
        target_info = get_probe_info(this_target)
        print(target_info)
        if target_info == None:
            continue
        measurement_dict[this_measurement]['target_probe'] = target_info[0]
        measurement_dict[this_measurement]['target_lat'] = target_info[1]
        measurement_dict[this_measurement]['target_lon'] = target_info[2]
        measurement_dict[this_measurement]['target_asn'] = target_info[3]
        measurement_dict[this_measurement]['target_ip'] = target_info[4]
        measurement_dict[this_measurement]['target_isanchor'] = target_info[5]

        # Set up spreadsheet formats
        worksheet, workbook = create_spreadsheet(
            'spreadsheets/'+area+'/target_'+measurement_dict[this_measurement]['target_ip'])

        bold = workbook.add_format({'bold': True})
        red_fill = workbook.add_format({'bg_color': 'red'})
        orange_fill = workbook.add_format({'bg_color': 'orange'})
        border = workbook.add_format({'bg_color': 'orange'})
        row = 0
        col = 0

        min_dist = 1000000
        max_col = 0

        tl_time = 1000000
        it_time = 1000000
        il_time = 1000000
        sl_time = 1000000
        st_time = 1000000
        il_row = 0
        it_row = 0
        tl_row = 0
        sl_row = 0
        st_row = 0

        # get all hops data for each source probe
        for source_probe in probe_list:
            row += 1
            col = 0
            # if source and target are same skip
            print("probe is ", source_probe)
            if source_probe == this_target:
                continue
            measurement_dict[this_measurement][source_probe] = {}
            source_info = get_probe_info(source_probe)
            print(source_info)
            measurement_dict[this_measurement][source_probe]['lat'] = source_info[1]
            measurement_dict[this_measurement][source_probe]['lon'] = source_info[2]
            measurement_dict[this_measurement][source_probe]['asn'] = source_info[3]
            measurement_dict[this_measurement][source_probe]['ip'] = source_info[4]
            measurement_dict[this_measurement][source_probe]['is_anchor'] = source_info[5]
            measurement_dict[this_measurement][source_probe]['first_hop'] = 0
            measurement_dict[this_measurement][source_probe]['ixp_hop'] = 0
            measurement_dict[this_measurement][source_probe]['last_router_hop'] = 0
            measurement_dict[this_measurement][source_probe]['ixp_to_target_time'] = 0
            measurement_dict[this_measurement][source_probe]['ixp_to_last_router_time'] = 0
            min_s_to_lr_time = 1000000
            min_i_to_t_time = 1000000
            min_i_to_lr_time = 1000000
            min_t_to_lr_time = 1000000
            min_s_to_t_time = 1000000
            min_t_to_lr_row = 0
            min_i_to_t_row = 0
            min_i_to_lr_row = 0
            min_s_to_lr_row = 0
            min_s_to_t_row = 0

            worksheet.write_string(row, col, str(source_probe))
            col += 1
            hops = get_hops(this_measurement, source_probe)

            print(hops)
            if hops != []:
                first_hop = 0
                ixp_hop = 0
                last_router_hop = 0
                last_hop = int(len(hops))

                for h in range(last_hop):
                    hop = hops[h][3]
                    measurement_dict[this_measurement][source_probe][hop] = {}

                    measurement_dict[this_measurement][source_probe][hop]['rtt'] = hops[h][4]
                    measurement_dict[this_measurement][source_probe][hop]['hostname'] = hops[h][5]
                    measurement_dict[this_measurement][source_probe][hop]['prefix'] = hops[h][6]
                    measurement_dict[this_measurement][source_probe][hop]['ip'] = hops[h][7]
                    measurement_dict[this_measurement][source_probe][hop]['ip_id'] = hops[h][8]
                    measurement_dict[this_measurement][source_probe][hop]['est_hop_distance_to_source'] = measurement_dict[
                        this_measurement][source_probe][hop]['rtt'] / 2 * packet_speed
                    measurement_dict[this_measurement][source_probe]['total_hops'] = last_hop
                    worksheet.write(0, col, 'hop'+str(hop)+' ip', bold)

                    subnet = ''

                    if measurement_dict[this_measurement][source_probe][hop]['ip'] != None:
                        subnet = measurement_dict[this_measurement][source_probe][hop]['ip'].split(
                            '.')
                        subnet = subnet[0]+'.'+subnet[1]+'.'+subnet[2]
                        print(
                            'ip is ', measurement_dict[this_measurement][source_probe][hop]['ip'])
                        print("Subnet is", subnet)
                        if first_hop == '':
                            # TODO this needs to be set to check against STATIC variable local_subnets
                            if not measurement_dict[this_measurement][source_probe][hop]['ip'].startswith(('100.64.', '100.65.', '100.66.', '100.67.', '100.68.', '100.69.',
                            '100.70.', '100.71.', '100.72.', '100.73.', '100.74.', '100.75.', '100.76.', '100.77.', '100.78.',
                            '100.79.', '100.80.', '100.81.', '100.82.', '100.83.', '100.84.', '100.85.', '100.86.', '100.87.',
                            '100.88.', '100.89.', '100.90.', '100.91.', '100.92.', '100.93.', '100.94.', '100.95.', '100.96.',
                            '100.97.', '100.98.', '100.99.', '100.100.', '100.101.', '100.102.', '100.103.', '100.104.', '100.105.',
                            '100.106.', '100.107.', '100.108.', '100.109.', '100.110.', '100.111.', '100.112.', '100.113.', '100.114.',
                            '100.115.', '100.116.', '100.117.', '100.118.', '100.119.', '100.120.', '100.121.', '100.122.', '100.123.',
                            '100.124.', '100.125.', '100.126.', '100.127.',
                            '10.', '172.16.', '172.17.', '172.18.', '172.19.', '172.20.', '172.21.', '172.22.',
                            '172.23.', '172.24.', '172.25.', '172.26.', '172.27.', '172.28.', '172.29.', '172.30.', '172.31.', '192.168.')):
                                measurement_dict[this_measurement][source_probe]['first_hop'] = hop
                        # TODO this needs to be set to check against STATIC variable ipx_ips
                        if measurement_dict[this_measurement][source_probe][hop]['ip'].startswith(('196.223.14', '196.223.30', '196.10.140', '196.223.22', '196.10.141', '196.60.8', '196.60.9', '196.60.10', '196.60.11', '105.22.46')):
                            worksheet.write(
                                row, col, measurement_dict[this_measurement][source_probe][hop]['ip'], red_fill)
                            measurement_dict[this_measurement][source_probe]['ixp_hop'] = hop
                            # We also need to work out which facility of the IX is being used so What is the incoming and outgoing hops
                            measurement_dict[this_measurement][source_probe]['incoming_ixp_hop'] = hop-1
                            measurement_dict[this_measurement][source_probe]['outgoing_ixp_hop'] = hop+1
                            
                        else:
                            worksheet.write(
                                row, col, measurement_dict[this_measurement][source_probe][hop]['ip'])
                        worksheet.set_column(col, col, 15)
                        col += 1
                        worksheet.write(0, col, 'hop'+str(hop)+' rtt', bold)
                        worksheet.write(
                            row, col, measurement_dict[this_measurement][source_probe][hop]['rtt'])
                    else:
                        col += 1

                    # stt = float("{:.2f}".format(stt))
                    print("hop is", hop)
                    print('row, col  is ', row, col)
                    print(measurement_dict[this_measurement]
                          [source_probe][hop])

                    if not measurement_dict[this_measurement][source_probe][hop]['ip'] == None:
                        if not measurement_dict[this_measurement][source_probe][hop]['ip'].startswith(('100.64.', '100.65.', '100.66.', '100.67.', '100.68.', '100.69.',
                            '100.70.', '100.71.', '100.72.', '100.73.', '100.74.', '100.75.', '100.76.', '100.77.', '100.78.',
                            '100.79.', '100.80.', '100.81.', '100.82.', '100.83.', '100.84.', '100.85.', '100.86.', '100.87.',
                            '100.88.', '100.89.', '100.90.', '100.91.', '100.92.', '100.93.', '100.94.', '100.95.', '100.96.',
                            '100.97.', '100.98.', '100.99.', '100.100.', '100.101.', '100.102.', '100.103.', '100.104.', '100.105.',
                            '100.106.', '100.107.', '100.108.', '100.109.', '100.110.', '100.111.', '100.112.', '100.113.', '100.114.',
                            '100.115.', '100.116.', '100.117.', '100.118.', '100.119.', '100.120.', '100.121.', '100.122.', '100.123.',
                            '100.124.', '100.125.', '100.126.', '100.127.',
                            '10.', '172.16.', '172.17.', '172.18.', '172.19.', '172.20.', '172.21.', '172.22.',
                            '172.23.', '172.24.', '172.25.', '172.26.', '172.27.', '172.28.', '172.29.', '172.30.', '172.31.', '192.168.')):
                            if not measurement_dict[this_measurement][source_probe][hop]['ip'] == measurement_dict[this_measurement]['target_ip']:
                                measurement_dict[this_measurement][source_probe]['last_router_hop'] = hop
                    col += 1
                    if max_col < col:
                        max_col = col
                #################################################################################################
                # END of HOP Loop
                #################################################################################################

                max_col = 50

                # Calculate IXP to Target time if Path goes through an IXP
                ixp_hop = measurement_dict[this_measurement][source_probe]['ixp_hop']
                if ixp_hop:
                    # Calculate time from IXP to target
                    measurement_dict[this_measurement][source_probe]['ixp_to_target_time'] = measurement_dict[this_measurement][
                        source_probe][last_hop]['rtt'] - measurement_dict[this_measurement][source_probe][ixp_hop]['rtt']
                    if measurement_dict[this_measurement][source_probe]['ixp_to_target_time'] < min_i_to_t_time:
                        min_i_to_t_time = measurement_dict[this_measurement][source_probe]['ixp_to_target_time']
                        min_i_to_t_row = row
                last_router_hop = measurement_dict[this_measurement][source_probe]['last_router_hop']

                if last_router_hop:
                    # Calculate time from target to last router
                    measurement_dict[this_measurement][source_probe]['target_to_last_router_time'] = measurement_dict[this_measurement][
                        source_probe][last_hop]['rtt'] - measurement_dict[this_measurement][source_probe][last_router_hop]['rtt']
                    print('min_t_to_lr_row_before',
                          min_t_to_lr_row, min_t_to_lr_time)
                    if measurement_dict[this_measurement][source_probe]['target_to_last_router_time'] < min_t_to_lr_time:
                        min_t_to_lr_time = measurement_dict[this_measurement][
                            source_probe]['target_to_last_router_time']
                        min_t_to_lr_row = row
                        print('min_t_to_lr_row_after',
                              min_t_to_lr_row, min_t_to_lr_time)
                        orange(workbook, worksheet, row, last_router_hop*2-1)
                        # box(workbook,worksheet,row,last_router_hop*2-1,1,1)
                    # Calculate time from source to last router
                    if measurement_dict[this_measurement][source_probe][last_router_hop]['rtt'] < min_s_to_lr_time:
                        min_s_to_lr_time = measurement_dict[this_measurement][source_probe][last_router_hop]['rtt']
                        min_s_to_lr_row = row

                if last_router_hop and ixp_hop:
                    print('lr,ixp', last_router_hop, ixp_hop)
                    # Calculate time from IXP to last router
                    measurement_dict[this_measurement][source_probe]['ixp_to_last_router_time'] = measurement_dict[this_measurement][
                        source_probe][last_router_hop]['rtt'] - measurement_dict[this_measurement][source_probe][ixp_hop]['rtt']
                    if measurement_dict[this_measurement][source_probe]['ixp_to_last_router_time'] < min_i_to_lr_time:
                        min_i_to_lr_time = measurement_dict[this_measurement][source_probe]['ixp_to_last_router_time']
                        min_i_to_lr_row = row
                        # print ('min_i_to_lr_row', min_i_to_lr_row,min_i_to_lr_time)

                # If this rtt < than the lowest source to target time then this si the quickest so far 
                if measurement_dict[this_measurement][source_probe][last_hop]['rtt'] < min_s_to_t_time:
                    min_s_to_t_time = measurement_dict[this_measurement][source_probe][last_hop]['rtt']
                    min_s_to_t_row = row
                # If this ixp to target time < than the lowest ixp to target time then this is the quickest it_time so far 
                if min_i_to_t_time > 0 and min_i_to_t_time < it_time:
                    it_time = min_i_to_t_time
                    it_row = row
                worksheet.write(0, max_col+1, 'i_to_t', bold)
                worksheet.write(row, max_col+1, min_i_to_t_time, bold)
                worksheet.set_column(max_col+1, max_col+1, 15)
                # If this ixp to last hop router time < than the lowest ixp to last hop router time then this is the quickest il_time so far 
                if min_i_to_lr_time > 0 and min_i_to_lr_time < il_time:
                    il_time = min_i_to_lr_time
                    il_row = row
                worksheet.write(0, max_col+2, 'i_to_lr', bold)
                worksheet.write(row, max_col+2, min_i_to_lr_time, bold)
                worksheet.set_column(max_col+2, max_col+2, 15)
                # If this target to last hop router time < than the lowest target to last hop router time then this is the quickest tl_time so far 
                if min_t_to_lr_time > 0 and min_t_to_lr_time < tl_time:
                    tl_time = min_t_to_lr_time
                    tl_row = row
                worksheet.write(0, max_col+3, 't_to_lr', bold)
                worksheet.write(row, max_col+3, min_t_to_lr_time, bold)
                worksheet.set_column(max_col+3, max_col+3, 15)

                # If this source to last hop router time < than the lowest source to last hop router time then this is the quickest sl_time so far
                if min_s_to_lr_time > 0 and min_s_to_lr_time < sl_time:
                    sl_time = min_s_to_lr_time
                    sl_row = row
                worksheet.write(0, max_col+4, 's_to_lr', bold)
                worksheet.write(row, max_col+4, min_s_to_lr_time, bold)
                worksheet.set_column(max_col+4, max_col+4, 15)

                 # If this source to target time < than the lowest source to target time then this is the quickest st_time so far
                if min_s_to_t_time > 0 and min_s_to_t_time < st_time:
                    st_time = min_s_to_t_time
                    st_row = row
                worksheet.write(0, max_col+5, 's_to_t', bold)
                worksheet.write(row, max_col+5, min_s_to_t_time, bold)
                worksheet.set_column(max_col+5, max_col+5, 15)

        #######################################################################################################
        # END of Measurement Loop
        # ####################################################################################################
        '''
        worksheet.write(0,max_col+5,'Min dist to tgt',bold)
        worksheet.write(min_row,max_col+5, min_dist, bold)
        worksheet.set_column(max_col+5,max_col+5,15)
        worksheet.write(0,max_col+6,'from_IXP',bold)
        worksheet.write(min_row,max_col+6, str(from_ixp), bold)
        worksheet.set_column(max_col+6,max_col+6,15)
        '''

        if it_time > 0:
            box(workbook, worksheet, it_row, max_col+1, 1, 1)
        if il_time > 0:
            box(workbook, worksheet, il_row, max_col+2, 1, 1)
        if tl_time > 0:
            box(workbook, worksheet, tl_row, max_col+3, 1, 1)
        if sl_time > 0:
            box(workbook, worksheet, sl_row, max_col+4, 1, 1)
        if st_time > 0:
            box(workbook, worksheet, st_row, max_col+5, 1, 1)

        '''
        name = worksheet.get_name()

        print(name)
        box(workbook,worksheet,min_row,1,1,max_col+5)
        print()
        '''

        workbook.close()
        ##########################################################################################################
        # END of seperate workbooks
        ##########################################################################################################

        # Create the overall spreadsheet
        
        # Reset all variables
        last_router_hop = ''
        ixp_hop = ''
        subnet= ''
        lat_src = ''
        lon_src = ''
        lat_ixp = ''
        lon_ixp = ''
        name_ixp = ''
        lhr_ip_address = ''
 
        
        
        
        o_row += 1
        print('********************************************************************************************')
        print('o_row', o_row)
        overall_ws.write(
            o_row, 0, measurement_dict[this_measurement]['target_ip'])
        overall_ws.write(
            o_row, 1, measurement_dict[this_measurement]['target_probe'])
        overall_ws.write(
            o_row, 2, measurement_dict[this_measurement]['target_lat'])
        overall_ws.write(
            o_row, 3, measurement_dict[this_measurement]['target_lon'])
        overall_ws.write(o_row, 4, tl_time)

        # Also add the important results to results dict for map
        target_ip_address = measurement_dict[this_measurement]['target_ip']
        lat_tgt = measurement_dict[this_measurement]['target_lat']
        lon_tgt = measurement_dict[this_measurement]['target_lon']
        target_id = measurement_dict[this_measurement]['target_probe']
        results_dict[target_ip_address]={}
        results_dict[target_ip_address]['lat']=lat_tgt
        results_dict[target_ip_address]['lon']=lon_tgt
        results_dict[target_ip_address]['id']=target_id
        results_dict[target_ip_address]['time_to_lr'] = tl_time

        



        # Write Geo Location of IXP used by target
        probe=probe_list[tl_row-1]
        last_router_hop=measurement_dict[this_measurement][probe]['last_router_hop']
        ixp_hop=measurement_dict[this_measurement][probe]['ixp_hop']
        
        if ixp_hop:
            subnet=measurement_dict[this_measurement][probe][ixp_hop]['ip'].split(
                '.')
            subnet=subnet[0]+'.' + subnet[1]+'.'+subnet[2]
            sql="SELECT ixp_id FROM ixp_ips WHERE ip_address = %s"
            val=(subnet,)
            cursor.execute(sql, val)
            id=cursor.fetchone()
            sql="SELECT lat, lon FROM ixps WHERE id = %s"
            val=(id[0],)
            cursor.execute(sql, val)
            myresult=cursor.fetchone()

            overall_ws.write(
                o_row, 5, measurement_dict[this_measurement][probe][ixp_hop]['ip'])
            overall_ws.write(o_row, 6, myresult[0])
            overall_ws.write(o_row, 7, myresult[1])



        # Write Geo location of source probe
        if last_router_hop:
            overall_ws.write(
                o_row, 8, measurement_dict[this_measurement][probe][last_router_hop]['ip'])

        overall_ws.write(o_row, 9, st_time)
        probe=probe_list[st_row-1]
        last_router_hop=measurement_dict[this_measurement][probe]['last_router_hop']
        ixp_hop=measurement_dict[this_measurement][probe]['ixp_hop']
        overall_ws.write(
            o_row, 10, measurement_dict[this_measurement][probe]['ip'])
        overall_ws.write(o_row, 11, probe)
        overall_ws.write(
            o_row, 12, measurement_dict[this_measurement][probe]['lat'])
        overall_ws.write(
            o_row, 13, measurement_dict[this_measurement][probe]['lon'])

        if ixp_hop:
            subnet=measurement_dict[this_measurement][probe][ixp_hop]['ip'].split(
                '.')
            subnet=subnet[0]+'.' + subnet[1]+'.'+subnet[2]
            sql="SELECT ixp_id FROM ixp_ips WHERE ip_address = %s"
            val=(subnet,)
            cursor.execute(sql, val)
            id=cursor.fetchone()
            sql="SELECT lat, lon FROM ixps WHERE id = %s"
            val=(id[0],)
            cursor.execute(sql, val)
            myresult=cursor.fetchone()
            overall_ws.write(
                o_row, 14, measurement_dict[this_measurement][probe][ixp_hop]['ip'])
            overall_ws.write(o_row, 15, myresult[0])
            overall_ws.write(o_row, 16, myresult[1])
            lat_src=myresult[0]
            lon_src=myresult[1]


        if last_router_hop:
            overall_ws.write(
                o_row, 17, measurement_dict[this_measurement][probe][last_router_hop]['ip'])

        overall_ws.write(o_row, 18, sl_time)
        probe=probe_list[sl_row-1]
        last_router_hop=measurement_dict[this_measurement][probe]['last_router_hop']
        ixp_hop=measurement_dict[this_measurement][probe]['ixp_hop']
        overall_ws.write(
            o_row, 19, measurement_dict[this_measurement][probe]['ip'])
        overall_ws.write(o_row, 20, probe)
        overall_ws.write(
            o_row, 21, measurement_dict[this_measurement][probe]['lat'])
        overall_ws.write(
            o_row, 22, measurement_dict[this_measurement][probe]['lon'])
        if ixp_hop:
            subnet=measurement_dict[this_measurement][probe][ixp_hop]['ip'].split(
                '.')
            subnet=subnet[0]+'.' + subnet[1]+'.'+subnet[2]
            sql="SELECT ixp_id FROM ixp_ips WHERE ip_address = %s"
            val=(subnet,)
            cursor.execute(sql, val)
            id=cursor.fetchone()
            sql="SELECT lat, lon FROM ixps WHERE id = %s"
            val=(id[0],)
            cursor.execute(sql, val)
            myresult=cursor.fetchone()




            overall_ws.write(
                o_row, 23, measurement_dict[this_measurement][probe][ixp_hop]['ip'])
            overall_ws.write(o_row, 24, myresult[0])
            overall_ws.write(o_row, 25, myresult[1])
        if last_router_hop:
            overall_ws.write(
                o_row, 26, measurement_dict[this_measurement][probe][last_router_hop]['ip'])

        overall_ws.write(o_row, 27, il_time)
        probe=probe_list[il_row-1]
        last_router_hop=measurement_dict[this_measurement][probe]['last_router_hop']
        ixp_hop=measurement_dict[this_measurement][probe]['ixp_hop']
        if ixp_hop:
            subnet=measurement_dict[this_measurement][probe][ixp_hop]['ip'].split(
                '.')
            subnet=subnet[0]+'.' + subnet[1]+'.'+subnet[2]
            sql="SELECT ixp_id FROM ixp_ips WHERE ip_address = %s"
            val=(subnet,)
            cursor.execute(sql, val)
            id=cursor.fetchone()
            sql="SELECT lat, lon,name FROM ixps WHERE id = %s"
            val=(id[0],)
            cursor.execute(sql, val)
            myresult=cursor.fetchone()
            overall_ws.write(o_row, 28, measurement_dict[this_measurement][probe][ixp_hop]['ip'])
            overall_ws.write(o_row, 29, myresult[0])
            overall_ws.write(o_row, 30, myresult[1])
            

            


            lat_ixp = myresult[0]
            lon_ixp = myresult[1]
            name_ixp = myresult[2]
            
            results_dict[target_ip_address][name_ixp]= {} 
            results_dict[target_ip_address][name_ixp]['ip'] = measurement_dict[this_measurement][probe][ixp_hop]['ip']
            results_dict[target_ip_address][name_ixp]['lat']=lat_ixp
            results_dict[target_ip_address][name_ixp]['lon']=lon_ixp
            results_dict[target_ip_address][name_ixp]['time_to_lr'] = il_time
            lhr_ip_address = measurement_dict[this_measurement][probe][last_router_hop]['ip']
            results_dict[target_ip_address][lhr_ip_address] = {}
        
            
        if last_router_hop:
            overall_ws.write(
                o_row, 31, measurement_dict[this_measurement][probe][last_router_hop]['ip'])

        overall_ws.write(o_row, 32, it_time)
        probe=probe_list[it_row-1]
        last_router_hop=measurement_dict[this_measurement][probe]['last_router_hop']
        ixp_hop=measurement_dict[this_measurement][probe]['ixp_hop']
        if ixp_hop:
            subnet=measurement_dict[this_measurement][probe][ixp_hop]['ip'].split(
                '.')
            subnet=subnet[0]+'.' + subnet[1]+'.'+subnet[2]
            sql="SELECT ixp_id FROM ixp_ips WHERE ip_address = %s"
            val=(subnet,)
            cursor.execute(sql, val)

            id=cursor.fetchone()
            print(subnet, id)
            sql="SELECT lat, lon FROM ixps WHERE id = %s"
            val=(id[0],)
            cursor.execute(sql, val)
            myresult=cursor.fetchone()
            overall_ws.write(
                o_row, 33, measurement_dict[this_measurement][probe][ixp_hop]['ip'])
            overall_ws.write(o_row, 34, myresult[0])
            overall_ws.write(o_row, 35, myresult[1])
        if last_router_hop:
            overall_ws.write(
                o_row, 36, measurement_dict[this_measurement][probe][last_router_hop]['ip'])
        

        # calculate estimated distance to last hop router from ixp (ie radius of circle)
        rtt=il_time
        # Average Speed of packet though fibre cable 2/3C  = 200 km per millisecond
        speed=.66 * 300000
        stt=rtt/2                                                     # Single trip time
        # Distance packet travelled at this speed
        distance_il=stt * speed

        # calculate estimated distance to last hop router from target (ie radius of circle)
        rtt=tl_time
        # Average Speed of packet though fibre cable 2/3C  = 200 km per millisecond
        speed=.66 * 300000
        stt=rtt/2                                                     # Single trip time
        # Distance packet travelled at this speed
        distance_tl=stt * speed

        # if no IXP then calculate topgrapical distance to last hop router from source (ie radius of circle)
        rtt=sl_time
        # Average Speed of packet though fibre cable 2/3C  = 200 km per millisecond
        speed=.66 * 300000
        stt=rtt/2                                                     # Single trip time
        # Distance packet travelled at this speed
        distance_sl=stt * speed
         # write estimated distance between ixp and last hop, target and last hop, source and last hop
        print(measurement_dict[this_measurement]['target_ip'], 'il', distance_il, 'tl', distance_tl,'sl',distance_sl)      
        overall_ws.write(o_row, 37, distance_il)
        overall_ws.write(o_row, 38, distance_tl)
        overall_ws.write(o_row, 39, distance_sl)

        #######################################################################################################
        # Now Calculate the estimated position of the last hop router from the source or ixp geolocation and  #
        # the target geo location                                                                             #
        # See https://scipython.com/book/chapter-8-scipy/problems/p84/overlapping-circles/                    #
        #######################################################################################################    


        # Calculate Actual distance between ixp/source and target
        if ixp_hop:
            actual_it_distance= check_distance(lon_ixp, lat_ixp, lon_tgt, lat_tgt)
            print('actual Distance from ixp to target', actual_it_distance)
            #actual_st_distance= check_distance(lon_src, lat_src, lon_tgt, lat_tgt)
            #print('actual Distance from source to target', actual_st_distance)
            overall_ws.write(o_row, 40, actual_it_distance)
            #overall_ws.write(o_row, 41, actual_st_distance)

            #distance_to_lhr = find_d(actual_it_distance,distance_il,distance_tl)
            
            #print('Distance to lhr', distance_to_lhr)
        print(lon_ixp, lat_ixp, lon_tgt, lat_tgt)
        print(target_ip_address,lhr_ip_address)
        if lhr_ip_address:
            results_dict[target_ip_address][lhr_ip_address]['lat'] = 0 # TODO Some mathemeatical formulae to work out the area that the LHR falls in 
            results_dict[target_ip_address][lhr_ip_address]['lon'] = 0 # TODO See above


        overall_wb.close()
        print(results_dict)
        ###########################################################################
        # Now create the Webpage
        ###########################################################################

        target_ip = target_ip_address
        target_id = results_dict[target_ip_address]['id'] 
        target_asn = measurement_dict[this_measurement]['target_asn'] 
        target_isanchor = measurement_dict[this_measurement]['target_isanchor'] 

        # if probe is an anchor then no inaccuracy radius is required
        # If probe is  not an anchor then have set radius to 10km (my own observed inaccuracy) 
        if target_isanchor:
            target_inaccuracy = 0   # Default size of placement is 100 metres
        else:
            target_inaccuracy = 900 # default is 100metres plus 900metres = 1k, See https://atlas.ripe.net/about/faq/#are-the-locations-of-probes-made-public

        # Create HTML file and copy header info into it
        filename = 'targets/southafrica/'+target_ip+'.html'
        cmd = 'cp html/head.html ' + filename
        os.system(cmd)

        # Fix File Permisssions
        cmd = 'chmod ' + '766 ' + filename
        os.system(cmd)

        # Write Target latitude and longitude to html file for zoom location
        
        lat = results_dict[target_ip]['lat']
        lon = results_dict[target_ip]['lon']
        myfile = open(filename, 'a')
        myfile.write(str(lat)+", "+str(lon)+'], 12);\n')
        myfile.close()

        # write tilelayer information to html file
        cmd = 'cat html/tilelayer.html >> ' + filename
        os.system(cmd)


        # create ipaddress points on map in green circles
        stringa = "      var circle"
        stringb = " = L.circle(["
        string1 = "      // show the area of operation of the AS on the map\n      var polygon = L.polygon([\n"
        string2 = "], { color: 'red', fillColor: '#00', interactive: false, fillOpacity: 0.0, radius: "
        stringgreen = "], { color: 'green', fillColor: '#8000000', fillOpacity: 0.5, radius: "
        stringgreen2 = "], { color: 'green', fillColor: '#000000', fillOpacity: 0, radius: "
        stringred = "], { color: 'red', fillColor: '#8000000', fillOpacity: 0.5, radius: "
        stringorange = "], { color: 'orange', fillColor: 'orange', fillOpacity: 0.5, radius: "
        string25 = "], { color: 'yellow', fillColor: '#8000000', fillOpacity: 0.5, radius: "
        string2a = " }).addTo(map);"

        string3 = "        ]).addTo(map);\n"
        string4 = '      polygon.bindPopup("<b>AS'
        string5 = '</b><br />'
        string6 = '<br />Area of Operation");\n'
        string7 = '      circle.bindPopup("<b>Probe '
        string7a = '      circle'
        string7b = '.bindPopup("<b> '
        string7c = '.bindPopup("<b>IXP '
        string8 = ' ").openPopup();\n\n'
        string8a = ' ");\n\n'
        spacer1 = "        ["
        spacer2 = "],\n"

        


        
        
        
        
        values = list(results_dict[target_ip].items())
        
        print ('value',values)
        if len(values) > 4:
            myfile = open(filename, 'a')    
            ixp_name = values[4][0]
            ixp_ip =  results_dict[target_ip][ixp_name]['ip']
            ixp_lat = results_dict[target_ip][ixp_name]['lat']
            ixp_lon = results_dict[target_ip][ixp_name]['lon']
            ixp_to_lr = results_dict[target_ip][ixp_name]['time_to_lr']/2
            lr_ip = values[5][0]
        
            # Create orange IXP to Target circle - These are Actual Location of target probes/anchors 
            myfile.write(stringa + '2'+stringb+str(ixp_lat) +
                    ','+str(ixp_lon)+stringorange+str(distance_il+distance_tl)+string2a+'\n')
            # Create orange Popup
            myfile.write(string7a + '2'+string7b+'Estimated Target Location from Last hop Router '+target_ip + string5 + 'AS ' +
                    str(target_asn)+ string5 + 'Distance to Target from LHR: '+str(distance_tl)+string8a)


            
            # Create Red IP to LHR circle - These are Actual Location of target probes/anchors 
            myfile.write(stringa + '2'+stringb+str(ixp_lat) +
                    ','+str(ixp_lon)+stringred+str(100+distance_il)+string2a+'\n')
            # Create Red Popup
            myfile.write(string7a + '2'+string7b+'Estimated Last Hop Router Location' +string5+'IXP IP:'+str(ixp_ip) +string5+'LHR IP: '+ lr_ip  + string5 + 'AS ' +
                    str(target_asn)+ string5 + 'Distance to LHR from IXP: '+str(distance_il)+ string8a)
            

            # Create Green Target location - These are Actual Location of target probes/anchors 
            
            myfile.write(stringa + '1'+stringb+str(lat) +
                    ','+str(lon)+stringgreen+str(100+target_inaccuracy)+string2a+'\n')
            # Create Green Popup
            myfile.write(string7a + '1'+string7b+'Actual Target Location '+target_ip + string5 + 'Probe '+str(target_id)+string5 + 'AS ' +
                    str(target_asn)+' Distance to last hop: '+ str(distance_tl)+string8a)
            
            # Create Green Target Area - this is the distance from target to LHR plus any inaccuracy due to RIPE owner privacy 
            #myfile.write(stringa + '1a'+stringb+str(lat) +
            #         ','+str(lon)+stringgreen2+str(distance_tl+ina)+string2a+'\n')

            # show all Internet Exchange Points on map

            myfile = open(filename, 'a')
            sql="SELECT * FROM ixps"
            cursor.execute(sql)
            myresult=cursor.fetchall()

            for ixp in myresult:
                # Create Red IXP circle - These are Actual Locations of IXP's 
                myfile.write(stringa + '_i'+str(ixp[0])+stringb+str(ixp[6]) +
                    ','+str(ixp[7])+stringred+'100'+string2a+'\n')
                myfile.write(string7a + '_i'+str(ixp[0])+string7c+str(ixp[1]) + string5 + ' '+str(ixp[2]) + ' '+str(ixp[3]) + string8a)

            
            # Complete Script and write to file
            #ip.write(string7 +'asnumber'+string5+'owner'+string8)




            string9 = "    </script>\n  </body>\n</html>"
            myfile.write (string9)
            myfile.close()
            print ('Copy ',filename,' upto web server')

            

            link1_string = '<p><a href="'
            link2_string = '">'
            link3_string = '</a></p>'

            menu.write(link1_string + 'http://icloud9.co.uk/phd/sa/'+target_ip +'.html' +link2_string +'Probe : '+str(target_id)+ 'Target IP : ' +target_ip+' '  + link3_string+'\n')

    
    menu.write('</body>\n</html>')
    menu.close()


    




        


        






        



