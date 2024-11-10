from backend.maps import get_directions, Location

Location(42.7277084,-73.6771619)
directions = get_directions(Location(42.7277084,-73.6771619), "ChIJoatIWSMP3okRxPawz9PkE-g")
for step in directions['routes'][0]['legs'][0]['steps']:
    print(step)