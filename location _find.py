#code used to determine your location to feed data into  the location class
#@author Rothang Ralefaso
#version 1.0
import geocoder
import requests
import folium
import csv
import os
import urllib.parse
import time 
import pandas as pd

name_user = input("input your full name : ")
location = geocoder.ipinfo('me')
city = location.city
latitude = location.latlng[0]  # Latitude
longitude = location.latlng[1]  # Longitude
country = location.country  #country


map_of_area = folium.Map(location=(latitude,longitude),zoom_start=12)
folium.Marker(
    location=[latitude,longitude ],
    tooltip="you",
    popup=name_user,
    icon=folium.Icon(icon="user", prefix="fa")
).add_to(map_of_area)

map_of_area.save("save_data/index.html")

# Printing the current location (just for testing/debugging)
#print(f"Your current location: {city} (Lat: {latitude}, Lon: {longitude}, Country: {country})")


try:
    radius = int(input("\nhow far are you willing to go,in meters (default 5000): ") or 5000)
except ValueError:
    print("\nInvalid input. Defaulting to 5000 meters.\n")
    radius = 5000



type_of_places = [
    "hospital",
    "general hospital",
    "specialty hospital",
    "clinic",
    "primary care clinic",
    "urgent care clinic",
    "specialty clinic",
    "mental health clinic",
    "physician practice",
    "private practice",
    "group practice",
    "nursing home",
    "home health care agency",
    "rehabilitation center",
    "physical rehabilitation center",
    "substance abuse treatment center",
    "speech and occupational therapy center",
    "pharmacy",
    "retail pharmacy",
    "compounding pharmacy",
    "online pharmacy",
    "laboratory",
    "clinical lab",
    "diagnostic imaging center",
    "ambulance service",
    "dental provider",
    "dentist",
    "orthodontist",
    "oral surgeon",
    "optometry provider",
    "optometrist",
    "ophthalmologist",
    "optician",
    "pharmaceutical company",
    "health insurance provider",
    "ambulatory surgical center",
    "palliative and hospice care provider",
    "veterinary service",
    "alternative and complementary care provider",
    "chiropractor",
    "acupuncturist",
    "massage therapist",
    "naturopath",
    "health technology and telemedicine provider",
    "telehealth platform",
    "health software provider",
    "blood bank & organ transplant center",
    "public health and government health agency",
    "cdc (center for disease control and prevention)",
    "fda (food and drug administration)",
    "local health department",
    "physical therapy center"
]


for i, place in enumerate(type_of_places, 1):
    print(f"[{i}] {place}")

try:
    type_of_place_choice = int(input(f"\nChoose your place type [1-{len(type_of_places)}]: "))
    type_of_place = type_of_places[type_of_place_choice - 1]
    print("\nyou have chosen: "+type_of_place)
except (ValueError, IndexError):
    print(f"Invalid choice, defaulting to 'Hospitals'.")
    type_of_place = "hospital"


# Retry mechanism with exponential backoff for API request
def get_nearby_places(url, retries=5, delay=5):
    attempt = 0
    while attempt < retries:
        try:
            response = requests.get(url, headers={'User-Agent': 'KR-AID/1.0 (mailto:devubusual@outlook.com)'})
            if response.status_code == 200:
                return response
            elif response.status_code == 429:  # Rate limit exceeded
                print(f"Rate limit exceeded. Retrying in {delay} seconds...")
                time.sleep(delay)
                delay *= 2  # Exponential backoff
            else:
                print(f"Error: Received status code {response.status_code}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Network error occurred: {e}. Retrying...")
            time.sleep(delay)
            delay *= 2
        attempt += 1
    return None


query = f"[out:json];(node(around:{radius},{latitude},{longitude})[amenity={type_of_place}];way(around:{radius},{latitude},{longitude})[amenity={type_of_place}];relation(around:{radius},{latitude},{longitude})[amenity={type_of_place}];);out;"
# URL-encode the query
encoded_query = urllib.parse.quote(query)
# Construct the final URL
url = f"https://overpass-api.de/api/interpreter?data={encoded_query}"

#print("Requesting URL:", url) #debugging purposes
response = get_nearby_places(url)

# Check if the CSV exists, and delete it if it does
csv_file_path = 'save_data/places_data.csv'

if os.path.exists(csv_file_path):
    os.remove(csv_file_path)  # Delete the existing file

if response:
    try:
        data = response.json()
        if 'elements' in data and data['elements']:
            # Open a new CSV file for writing
            with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['name', 'lat', 'lon', 'address', 'phone'])  # Writing header

                for place in data['elements']:
                    name = place.get('tags', {}).get('name', 'N/A')
                    lat = place.get('lat', None)  # None if lat is missing
                    lon = place.get('lon', None)  # None if lon is missing
                    address = place.get('address', 'N/A')
                    phone = place.get('tags', {}).get('phone', 'N/A')  # Check for phone number


                    print(f"\nName: {name}")
                    print(f"Latitude: {lat}, Longitude: {lon}")
                    print(f"Address: {address}")
                    print(f"Phone: {phone}")
                    print("-" * 30)

 
                    # Write place data to the CSV
                    writer.writerow([name, lat, lon, address, phone])  # Writing place data with phone number

        else:
            print(f"No nearby {type_of_place} found within {radius} meters.")
    except Exception as e:
        print(f"Error parsing JSON: {e}")
else:
    print("Failed to retrieve data after multiple attempts.")




updated_data = [] # for updaing csv
# Load the CSV file
df = pd.read_csv('save_data/places_data.csv')

def get_coordinates(place_name):
    g = geocoder.osm(place_name)  # Using OpenStreetMap geocoding
    if g.ok:
        return g.latlng  # Correctly return lat, lon
    else:
        return None


for index, row in df.iterrows():
    name = row['name']
    lat = row['lat']
    lon = row['lon']
    
    # Check if either latitude or longitude is missing or invalid
    if pd.isna(lat) or pd.isna(lon):
        print(f"Updating coordinates for {name}...")
        
        # Attempt to get coordinates from the place name
        lat, lon = get_coordinates(name+ ","+country)
        
        # If coordinates could not be retrieved, set lat/lon to None
        if lat is None or lon is None:
            print(f"Could not retrieve coordinates for {name}. Keeping previous data.")
            lat, lon = row['lat'], row['lon']
    
    # Update the row with the new lat/lon
    updated_data.append([name, lat, lon, row['address'], row['phone']])

# Create a new DataFrame with the updated data
updated_df = pd.DataFrame(updated_data, columns=['name', 'lat', 'lon', 'address', 'phone'])




# Save the updated DataFrame to a new CSV
updated_df.to_csv('save_data/updated_places_data.csv', index=False)
















""" if 'lat' in df.columns and 'lon' in df.columns:
    for index, row in df.iterrows():
        name = row['name']
        latitude = row['lat']
        longitude = row['lon']
        
        # Add a marker for each place
        folium.Marker(
            location=[latitude, longitude],
            popup=name,  # You can also show more info like the address or phone
            tooltip=name,  # Tooltip shows place name on hover
            icon=folium.Icon(icon='plus', icon_color='white', color='red') 
        ).add_to(map_of_area)

    # Save the map to an HTML file
    map_of_area.save("save_data/places_map.html")
    print("Map has been saved to 'places_map.html'.")
else:
    print("CSV file doesn't contain lat/lon columns.")

 """
