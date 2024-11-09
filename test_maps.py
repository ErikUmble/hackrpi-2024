import requests
import os
from dotenv import load_dotenv

load_dotenv()

MAP_API_KEY = os.getenv("MAP_API_KEY")

# Define the endpoint and parameters for nearby places search
endpoint = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"

# Location of interest (latitude, longitude)
location = "37.7749,-122.4194"  # Example: San Francisco, CA

# Search radius in meters
radius = 1500  # 1500 meters or 1.5 km

# Define the type of place you're interested in (optional)
place_type = "restaurant"

# Parameters for the API request
params = {
    "key": MAP_API_KEY,
    "location": location,
    "radius": radius,
    "type": place_type
}

# Send GET request to the Places API
response = requests.post(endpoint, params=params)
# Check if request was successful
if response.status_code == 200:
    # Parse JSON response
    print(response.json())
    places = response.json().get("results", [])
    for place in places:
        name = place.get("name")
        address = place.get("vicinity")
        print(f"Name: {name}, Address: {address}")
else:
    print(f"Error: {response.status_code}")