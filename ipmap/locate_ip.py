#!/usr/bin/env python

import json
import requests

key = "6f0e691d-056c-497d-9f5b-2297e970ec60"
target_ip = "129.232.223.26"
#target_ip = "196.60.8.152"
#endpoint = "https://ipmap.ripe.net/api/v1/locate/" + target_ip+ "/"
endpoint = "https://ipmap.ripe.net/api/v1/single-radius/" + target_ip+ "/"

response = requests.get(endpoint)

print (response.json())

# ipmap discovers ip address in Edenvale 22 km away from actual location Ferndale
# ping lcoation finds nearest probe to be near edenvale but estimated accuracy is 40km and the
# targets actual location falls within this 169.255.0.135
# -26.14095, 28.15247



