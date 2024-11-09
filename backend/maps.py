import requests
import os
from dotenv import load_dotenv

load_dotenv()

MAPS_API_KEY = os.getenv("MAPS_API_KEY")

class Location:
    def __init__(self, lat, lng):
        self.lat = lat
        self.lng = lng

    def __str__(self):
        return f"{self.lat},{self.lng}"

def get_nearby_places(lat, lng, radius, type):
    """
    Fetches nearby places using the older Google Maps Places API.

    Args:
        lat: Latitude of the center point.
        lng: Longitude of the center point.
        radius: Radius in meters around the center point.
        type: Type of places to search for.

    Returns:
        A list of nearby places, or None if an error occurs.
    """

    api_key = os.environ.get('MAPS_API_KEY')
    if not api_key:
        raise ValueError("GOOGLE_MAPS_API_KEY environment variable not set.")

    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lng}&radius={radius}&type={type}&key={api_key}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if data['status'] == 'OK':
            return data['results']
        else:
            print(f"Error: {data['status']}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None