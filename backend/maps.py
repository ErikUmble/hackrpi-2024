import requests
import os
from dotenv import load_dotenv

load_dotenv()

MAPS_API_KEY = os.getenv("MAPS_API_KEY")
if not MAPS_API_KEY:
    raise ValueError("MAPS_API_KEY environment variable not set.")


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

    
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lng}&radius={radius}&type={type}&key={MAPS_API_KEY}"

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
    
def get_directions(origin, destination, mode="walking"):
    """
    Fetches directions between two locations using the older Google Maps Directions API.

    Args:
        origin: Starting location as Location.
        destination: as a place_id str.

    Returns:
        A list of directions, or None if an error occurs.
    """

    url = "https://maps.googleapis.com/maps/api/directions/json"
    params = {
        "origin": str(origin),
        "destination": f"place_id:{destination}",
        "mode": mode,
        "key": MAPS_API_KEY,
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        if data['status'] == 'OK':
            return data
        else:
            print(f"Error: {data['status']}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def get_matching_place(lat, lng, query):
    """
    Returns the place_id of the place that best matches the name, near the current location.
    """

    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {
        "query": query,
        "location": f"{lat},{lng}",
        "key": MAPS_API_KEY,
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        if data['status'] == 'OK':
            places = response.json().get("results", [])

            # Get the best matching place (first result)
            if places:
                best_match = places[0]  # Best match is typically the first result
                place_id = best_match.get("place_id")
                return place_id
        else:
            print(f"Error: {data['status']}")
            return None
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None