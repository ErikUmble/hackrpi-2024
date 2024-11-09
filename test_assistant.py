from backend.assistant import query
from backend.maps import get_nearby_places, Location

session = {}
response = query("Where can I eat pizza nearby?", session, Location(42.7277084,-73.6771619))
print(response)