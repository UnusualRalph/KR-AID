#code used to determine your location to feed data into  the location class

import geocoder
import requests

location =  geocoder.ipinfo('me') # uses ip adress to find location
city = location.city
street = location.street

def find_in_city(hospital):
