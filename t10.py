import mysql.connector
import csv
import json
from decimal import Decimal

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="brindle7",
    database="ipgeo"
    )
cursor = mydb.cursor()


# Get all data from file    
with open("dictionary1.json") as file:
    data =json.load(file)


for measurement in data:
    target_id = str(data[measurement]['probe_id'])
    
    target_isanchor = data[measurement]['target_isanchor']
    
    print(measurement,target_id,target_isanchor)
    
    sql = "UPDATE probes SET isanchor = %s WHERE id = %s "
    val = (target_isanchor, target_id)

    cursor.execute(sql,val)
    print(cursor.rowcount,"Probe", target_id, " !record inserted.", target_isanchor)
    mydb.commit()
    