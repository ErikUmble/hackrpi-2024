from backend.maps import get_nearby_places

places = get_nearby_places(42.7277084,-73.6771619, 2000, "restaurant")
for place in places:
    print(place['name'], place.get('opening_hours'))