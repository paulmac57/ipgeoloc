# ipgeoloc

# To read a ping measurement
1. edit ipgeoloc1-ping.py and change measurement id.
2. run ipgeloc1-ping.py to create dictionary file
3. run html-create.py to create html file
4. upload html filer to webserver

# To Read a Traceroute emasurement
1. Edit ipgeoloc1-tr.py and change the measurement id
2. run ipgeoloc1-tr.py to create a local dictionary file (saves in keep using Ripe Atlas)
3. run testfile.py to select probes that are 5ms distant from target and create smaller probes file
4. run html_create_tr3.py to read in the probes file and create a html file
5. copy this html file to webserver

# to create a spreadsheet from traceroute measurement.
1. run print_json.py

