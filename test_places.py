from backend.maps import get_nearby_places

places = get_nearby_places(42.7277084,-73.6771619, 1000, "restaurant")

print(places)