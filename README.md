# ipgeoloc

=============================================
# Version 1 reads in a single measurement data which has been created manually and then creates a html file which can be uploaded to a webserver

# To read a ping measurement
1. edit ipgeoloc1-ping.py and change measurement id.
2. run ipgeloc1-ping.py to create dictionary file
3. run html-create.py to create html file
4. upload html filer to webserver

# To Read a Traceroute measurement
1. Edit ipgeoloc1-tr.py and change the measurement id
2. run ipgeoloc1-tr.py to create a local dictionary file (saves in keep using Ripe Atlas)
3. run testfile.py to select probes that are 5ms distant from target and create smaller probes file
4. run html_create_tr3.py to read in the probes file and create a html file
5. copy this html file to webserver

# to create a spreadsheet from traceroute measurement.
1. run print_json.py

=========================================================
# Version 2 reads in multiple measurements and loads the data to a database.

# To create a multiple measurements list
# creates traceroutes to every probe in probes_measurement_id from all probes in
# probes_measurement_id
1. edit create_measurements2.py and change output filename as required
2. Set the probes_measurement_id to the measurement containing the probes you want to use (you will have need to have manually created a measurement ON RIPE for this)
3. change the output filename which will contain a list of all the measurement ids created
4. Change the Desc at line 75
5. remove the safeguard
6. run create_measurements.py
7. this creates a list of the RIPE ATLAS measurements ID's in the measurements subfolder

# Once the meausremnts have completed running. Use the list of measurments file created above to load all data and save it to a dictionary file

1. edit ipgeoloc2-tr.py and change filename to that set as above
2. run ipgeoloc2-tr.py to create dictionary1.py

# To Create a Database of multiple measurements created by # the create_measurements.py program
1. edit create_ipgeo_db.py
2. set create_table and read_file to True
3. this will then read the dictionary1 file created above and create the tables (db needs to exists already)
and will then populate the tables with the data file created by ipgeoloc2-tr.py

