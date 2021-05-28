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
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="brindle7",
    database="ipgeo"
    )
    cursor = mydb.cursor()

    
    target_probe = '1000492'

    # Get measurement where above is the target probe
    sql = "SELECT id FROM measurements WHERE target_id = %s"
    val = (target_probe,)
    cursor.execute(sql, val)
    m = cursor.fetchone()
    print("measurement is", m)
    # get id, coords, ip, isanchor  of source probe