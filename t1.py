from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="aswindow")

hop_address = "Kranhaus 1, 50678 Köln, Germany"                                     # hop address for Anexia
location = geolocator.geocode(hop_address)
print("lat",location.latitude,"lon", location.longitude)