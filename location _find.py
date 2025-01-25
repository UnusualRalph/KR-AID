#code used to determine your location to feed data into  the location class
#@author Rothang Ralefaso
#version 1.0
import geocoder
import requests

location = geocoder.ipinfo('me')
city = location.city
latitude = location.latlng[0]  # Latitude
longitude = location.latlng[1]  # Longitude
country = location.country  #country



# Printing the current location (just for testing/debugging)
#print(f"Your current location: {city} (Lat: {latitude}, Lon: {longitude}, Country: {country})")


try:
    radius = int(input("how far are you willing to go,in meters (default 5000): ") or 5000)
except ValueError:
    print("Invalid input. Defaulting to 5000 meters.")
    radius = 5000

# where they may desire to go (makes it more specific)
area_name = input(f"Enter a specific neighborhood or district name (or press Enter to skip): ").strip()


type_of_places = [ # list of possible types to chose from
    "Hospitals",
    "General Hospitals",
    "Specialty Hospitals",
    "Clinics",
    "Primary Care Clinics",
    "Urgent Care Clinics",
    "Specialty Clinics",
    "Mental Health Clinics",
    "Physician Practices",
    "Private Practices",
    "Group Practices",
    "Nursing Homes",
    "Home Health Care Agencies",
    "Rehabilitation Centers",
    "Physical Rehabilitation Centers",
    "Substance Abuse Treatment Centers",
    "Speech and Occupational Therapy Centers",
    "Pharmacies",
    "Retail Pharmacies",
    "Compounding Pharmacies",
    "Online Pharmacies",
    "Laboratories",
    "Clinical Labs",
    "Diagnostic Imaging Centers",
    "Ambulance Services",
    "Dental Providers",
    "Dentists",
    "Orthodontists",
    "Oral Surgeons",
    "Optometry Providers",
    "Optometrists",
    "Ophthalmologists",
    "Opticians",
    "Pharmaceutical Companies",
    "Health Insurance Providers",
    "Ambulatory Surgical Centers",
    "Palliative and Hospice Care Providers",
    "Veterinary Services",
    "Alternative and Complementary Care Providers",
    "Chiropractors",
    "Acupuncturists",
    "Massage Therapists",
    "Naturopaths",
    "Health Technology and Telemedicine Providers",
    "Telehealth Platforms",
    "Health Software Providers",
    "Blood Banks & Organ Transplant Centers",
    "Public Health and Government Health Agencies",
    "CDC (Centers for Disease Control and Prevention)",
    "FDA (Food and Drug Administration)",
    "Local Health Departments",
    "Physical Therapy Centers"
]

for i, place in enumerate(type_of_places, 1):
    print(f"[{i}] {place}")

try:
    type_of_place_choice = int(input(f"Choose your place type [1-{len(type_of_places)}]: "))
    type_of_place = type_of_places[type_of_place_choice - 1]
except (ValueError, IndexError):
    print(f"Invalid choice, defaulting to 'Hospitals'.")
    type_of_place = "Hospitals"

# If the user entered an area name, include it in the query to focus on the specific area.
query = f"{type_of_place}"
if area_name:
    query += f"{area_name}"




url = f"https://nominatim.openstreetmap.org/search?format=json&q={query}&lat={latitude}&lon={longitude}&radius={radius}&countrycodes={country}" #find everything based on info

headers = {
    'User-Agent': 'KR-AID/1.0 (mailto:devubusual@outlook.com)'  # Use your actual app name and contact info
}


# Make request to Nominatim API
response = requests.get(url, headers=headers)
#print(response) #-checking if the check was succesful


# Check if the response is successful
if response.status_code == 200:
    try:
        # Parse the JSON response
        data = response.json()

        # If there are results, display them
        if data:
            for place in data:
                name = place.get('display_name', 'N/A')
                lat = place.get('lat', 'N/A')
                lon = place.get('lon', 'N/A')
                address = place.get('address', 'N/A')

                print(f"\nName: {name}")
                print(f"Latitude: {lat}, Longitude: {lon}")
                print(f"Address: {address}")
                print("-" * 30)
        else:
            print(f"No nearby {type_of_place} found within {radius} meters.")
            
            # Fallback: search again without the area filter if no results are found
            print("\nTrying search without the area filter...")
            fallback_url = f"https://nominatim.openstreetmap.org/search?format=json&q={type_of_place}&lat={latitude}&lon={longitude}&radius={radius}&countrycodes={country}"
            fallback_response = requests.get(fallback_url, headers=headers)
            if fallback_response.status_code == 200:
                fallback_data = fallback_response.json()
                if fallback_data:
                    print("Results found without area filter:")
                    for place in fallback_data:
                        name = place.get('display_name', 'N/A')
                        lat = place.get('lat', 'N/A')
                        lon = place.get('lon', 'N/A')
                        address = place.get('address', 'N/A')
                        print(f"\nName: {name}")
                        print(f"Latitude: {lat}, Longitude: {lon}")
                        print(f"Address: {address}")
                        print("-" * 50)
                else:
                    print("No results found even without the area filter.")
            else:
                print("Error fetching fallback data.")
    except Exception as e:
        print(f"Error parsing JSON: {e}")
else:
    print(f"Error: Received status code {response.status_code}")
    print("Raw response:")
    print(response.text)
