#code used to determine your location to feed data into  the location class
#@author Rothang Ralefaso
#version 1.0
import geocoder
import requests


location =  geocoder.ipinfo('me') # uses ip adress to find location
city = location.city
street = location.street
latitude = location.latlng[0]  # Latitude
longitude = location.latlng[1]  # Longitude

radius = 5000  # Search radius in meters - default distance

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
length_of_place_list = len(type_of_places)

for i in range(length_of_place_list):
    i=i+1
    print("["+str(i)+"] "+type_of_places[i-1]+"\n")

type_of_place_choie = input("depending on the length chose your place [1- "+str(length_of_place_list)+"]: ") 

type_of_place = type_of_places[int(type_of_place_choie)-1]

url = f"https://nominatim.openstreetmap.org/search?format=json&q={type_of_place}&lat={latitude}&lon={longitude}&radius={radius}" #find everything based on info

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

        # Check if we have any results
        if data:
            for place in data:
                name = place.get('display_name', 'N/A')
                lat = place.get('lat', 'N/A')
                lon = place.get('lon', 'N/A')
                address = place.get('address', 'N/A')

                print(f"Name: {name}")
                print(f"Latitude: {lat}, Longitude: {lon}")
                print(f"Address: {address}")
                print("-" * 50)
        else:
            print(f"No nearby {type_of_place} found within {radius} meters.")
    except Exception as e:
        print(f"Error parsing JSON: {e}")
else:
    print(f"Error: Received status code {response.status_code}")
    print("Raw response:")
    print(response.text)
