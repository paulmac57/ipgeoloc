# After reading in the South African Database this file fixes Geocordinates of the locations that have NULL balues

import mysql.connector
# use free Nominatum to dicover hop coordiantes from address
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="aswindow")
# USing chargeable Google if nominatum fails to find hop coordiantes https://pypi.org/project/geocoder/
import geocoder

from html_create_tr import Html_Create 
from geopy.distance import geodesic
from ipwhois import IPWhois
from pprint import pprint
def tidy_database():
    # get list of geos with no lat, lon coords
    '''
    sql = "select * from geo where lat is NULL"
    cursor.execute(sql, )
    results = cursor.fetchall()
    print(results)
    
    # sET WAVERLEY BUSIENSS PARK COORDS
    sql = "update geo set lat = -33.9432487373587, lon = 18.47017155189178 where address LIKE '%Waverley Business Park%'"
    cursor.execute(sql, )
    mydb.commit()
    # Set Teraco data environments
    sql = "update geo set lat = -26.136994066564835, lon = 28.198611769318493 where address LIKE '%5 Brewery St%'"
    cursor.execute(sql, )
    mydb.commit() 
    # set the campus, johannesburg
    sql = "update geo set lat = -26.04181385976509, lon = 28.022000458984675 where address LIKE '%57 Sloane St%'"
    cursor.execute(sql, )
    mydb.commit()
    #myresult = cursor.fetchall()
    #print (myresult)
    # set zambesi tower
    sql = "update geo set lat = -24.65366320, lon = 25.90355730 where address LIKE '%Zambezi Towers%'"
    cursor.execute(sql, )
    mydb.commit()
    # set Nordwyk
    sql = "update geo set lat = -25.95752810, lon = 28.12104580 where address LIKE '%Noordwyk%'"
    cursor.execute(sql, )
    mydb.commit()
    # set Telcom Sa
    sql = "update geo set lat = -25.74388400, lon = 28.18640000  where address LIKE '%PO Box 2753%'"
    cursor.execute(sql, )
    mydb.commit(

    
    # set government enclave
    sql = "update geo set lat = -24.65683570, lon = 25.90984150  where address LIKE '%Box 700%'"
    cursor.execute(sql, )
    mydb.commit()
    # set government enclave
    sql = "update geo set lat = -24.65683570, lon = 25.90984150  where address LIKE '%Box 700%'"
    cursor.execute(sql, )
    mydb.commit()
    
    # set Umhlanga Centre
    sql = "update geo set lat = -29.72632820, lon = 31.08347090  where address LIKE '%Umhlanga Centre%'"
    cursor.execute(sql, )
    mydb.commit()

    # set 372Oak Avenue
    sql = "update geo set lat = -26.08718270, lon = 28.00320220  where address LIKE '%372Oak Avenue%'"
    cursor.execute(sql, )
    mydb.commit()

    # set 4 Hans Schoeman
    sql = "update geo set lat = -26.09361190, lon = 27.98232390  where address LIKE '%4 Hans Schoeman%'"
    cursor.execute(sql, )
    mydb.commit()

    # set Studio 34
    sql = "update geo set lat = -33.91358500, lon = 18.41769300  where address LIKE '%Studio 34%'"
    cursor.execute(sql, )
    mydb.commit()

    # set Wynberg Mews
    sql = "update geo set lat = -34.00370000, lon = 18.46754000  where address LIKE '%Wynberg Mews%'"
    cursor.execute(sql, )
    mydb.commit()

    # set Afrihost HQ
    sql = "update geo set lat = -26.04610200, lon = 28.05983280  where address LIKE '%Afrihost HQ%'"
    cursor.execute(sql, )
    mydb.commit()

    # set Shop 8A
    sql = "update geo set lat = -28.55658000, lon = 29.77227600  where address LIKE '%Shop 8A%'"
    cursor.execute(sql, )
    mydb.commit()

    # set Box 2823
    sql = "update geo set lat = -34.07568990, lon = 18.84326560  where address LIKE '%Box 2823%'"
    cursor.execute(sql, )
    mydb.commit()

    # set Postnet Suite 397
    sql = "update geo set lat = -26.05639860, lon = 28.02446390  where address LIKE '%Postnet Suite 397%'"
    cursor.execute(sql, )
    mydb.commit()
    

    # set 61 Oak Av
    sql = "update geo set lat = -25.87817340, lon = 28.18735570  where address LIKE '%61 Oak Av%'"
    cursor.execute(sql, )
    mydb.commit() 
    
    
    # set 1 Beachway
    sql = "update geo set lat = -29.77643100, lon = 31.03620300  where address LIKE '%1 Beachway%'"
    cursor.execute(sql, )
    mydb.commit() 

    
    # set Townsend Office Park
    sql = "update geo set lat = -26.16910240, lon = 28.15799120  where address LIKE '%Townsend Office Park%'"
    cursor.execute(sql, )
    mydb.commit() 

    
    # set Monte Circle
    sql = "update geo set lat = -26.02665740, lon = 28.01310050  where address LIKE '%Monte Circle%'"
    cursor.execute(sql, )
    mydb.commit() 

    
    # set Boulevard Woodstock
    sql = "update geo set lat = -33.92941300, lon = 18.44972620  where address LIKE '%Boulevard Woodstock%'"
    cursor.execute(sql, )
    mydb.commit() 
    
   
    # set Belvedere Office Park
    sql = "update geo set lat = -33.86855040, lon = 18.64124040  where address LIKE '%Belvedere Office Park%'"
    cursor.execute(sql, )
    mydb.commit() 
   
    
    # set 1 Scott Street
    sql = "update geo set lat = -26.13623000, lon = 28.07039000  where address LIKE '%1 Scott Street%'"
    cursor.execute(sql, )
    mydb.commit() 

    
    # set Rhodes University
    sql = "update geo set lat = -33.31359110, lon = 26.51631350  where address LIKE '%Rhodes University%'"
    cursor.execute(sql, )
    mydb.commit() 

  
    # set Gemsbok Street
    sql = "update geo set lat = -27.73999000, lon = 29.92850000  where address LIKE '%Gemsbok Street%'"
    cursor.execute(sql, )
    mydb.commit() 

    
    # set Elektron Road
    sql = "update geo set lat = -33.96273560, lon = 18.83931530  where address LIKE '%Elektron Road%'"
    cursor.execute(sql, )
    mydb.commit() 

   
    # set Nickel Street
    sql = "update geo set lat = -22.62069990, lon = 17.08034850   where address LIKE '%Nickel Street%'"
    cursor.execute(sql, )
    mydb.commit() 

    
    # set Hammanshand road
    sql = "update geo set lat = -33.93280780, lon = 18.86444700    where address LIKE '%Hammanshand road%'"
    cursor.execute(sql, )
    mydb.commit()
 
    
    # set Solan Street
    sql = "update geo set lat = -33.93224910, lon = 18.42239810    where address LIKE '%Solan Street%'"
    cursor.execute(sql, )
    mydb.commit()

   
    # set Olympic Duel
    sql = "update geo set lat = -26.03707210, lon = 27.95580480    where address LIKE '%Olympic Duel%'"
    cursor.execute(sql, )
    mydb.commit()

    
    # set KAM Building
    sql = "update geo set lat = -1.29206590, lon = 36.82194620    where address LIKE '%KAM Building%'"
    cursor.execute(sql, )
    mydb.commit()

    
    # set Herndon
    sql = "update geo set lat = 38.96098290, lon = -77.37775100    where address LIKE '%Herndon%'"
    cursor.execute(sql, )
    mydb.commit()

    
    # set Global Av
    sql = "update geo set lat = 50.47501420, lon = 4.47710040    where address LIKE '%Global Av%'"
    cursor.execute(sql, )
    mydb.commit()

    
    # set Feldkirchner
    sql = "update geo set lat = 46.64122740, lon = 14.28915690    where address LIKE '%Feldkirchner%'"
    cursor.execute(sql, )
    mydb.commit()

   
    # set Raffles Tower
    sql = "update geo set lat = -20.24321770, lon = 57.49640780    where address LIKE '%Raffles Tower%'"
    cursor.execute(sql, )
    mydb.commit()

    
    # set Kingsway
    sql = "update geo set lat = 51.51325310, lon = -0.11797290    where address LIKE '%Kingsway%'"
    cursor.execute(sql, )
    mydb.commit()

    
    # set Julius Nyerere
    sql = "update geo set lat = -25.95214980, lon = 32.60356010    where address LIKE '%Julius Nyerere%'"
    cursor.execute(sql, )
    mydb.commit()

    
    # set Bekker Road
    sql = "update geo set lat = -26.01233740, lon = 28.11178590    where address LIKE '%Bekker Road%'"
    cursor.execute(sql, )
    mydb.commit()


    
    # set 180 Green Point
    sql = "update geo set lat = -33.90479100, lon = 18.40984510    where address LIKE '%180 Green Point%'"
    cursor.execute(sql, )
    mydb.commit()

    
    # set 392 Main Road
    sql = "update geo set lat = -26.05059840, lon = 28.02446010    where address LIKE '%392 Main Road%'"
    cursor.execute(sql, )
    mydb.commit()

    
    # set GOSWELL ROAD
    sql = "update geo set lat = 51.52900100927775, lon = -0.10084315952125335    where address LIKE '%GOSWELL ROAD%'"
    cursor.execute(sql, )
    mydb.commit()

    
    # set Paracon House
    sql = "update geo set lat = -26.063896741233528, lon = 27.970368707566504    where address LIKE '%Paracon House%'"
    cursor.execute(sql, )
    mydb.commit()

    
    # set Angola Cables , Cellwave
    sql = "update geo set lat = -8.913607388363989, lon = 13.181090263382593    where address LIKE '%Zona XR6B%'"
    cursor.execute(sql, )
    mydb.commit()

    
    # set Roggebaai
    sql = "update geo set lat = -33.9169623371522, lon = 18.42681069758983    where address LIKE '%Roggebaai%'"
    cursor.execute(sql, )
    mydb.commit()

    
    # set Edenvale 1609
    sql = "update geo set lat = -26.14508250, lon =28.15615330    where address LIKE '%Edenvale 1609%'"
    cursor.execute(sql, )
    mydb.commit()

    
    # set Woodmead 2191
    sql = "update geo set lat = -26.04741480, lon = 28.08007820    where address LIKE '%Woodmead 2191%'"
    cursor.execute(sql, )
    mydb.commit()

    
    # set Frosterley Crescent
    sql = "update geo set lat = -29.737190820945074, lon = 31.060661104338458    where address LIKE '%Frosterley Crescent%'"
    cursor.execute(sql, )
    mydb.commit()


    
    # set WA 98108-1226
    sql = "update geo set lat = 47.548721589513065, lon = -122.33191656005268    where address LIKE '%WA 98108-1226%'"
    cursor.execute(sql, )
    mydb.commit()


    
    # set Judges Court
    sql = "update geo set lat = -29.791301075535056, lon = 30.846055368652383    where address LIKE '%Judges Court%'"
    cursor.execute(sql, )
    mydb.commit()

    
    # set 35 Ebene
    sql = "update geo set lat = -20.24237200, lon = 57.49291530    where address LIKE '%35 Ebene%'"
    cursor.execute(sql, )
    mydb.commit()

    
    # set Witch-Hazel
    sql = "update geo set lat = -25.873771303359554, lon = 28.181289811441562    where address LIKE '%Witch-Hazel%'"
    cursor.execute(sql, )
    mydb.commit()

    '''





 
if __name__ == "__main__":
    
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="brindle7",
    database="ipgeo"
    )
    cursor = mydb.cursor(buffered=True)

    tidy_database()





