from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel
import json
from maps import get_nearby_places

load_dotenv()
client = OpenAI()

place_types = ['accounting', 'airport', 'amusement_park', 'aquarium', 'art_gallery', 'atm', 'bakery', 'bank', 'bar', 'beauty_salon', 'bicycle_store', 'book_store', 'bowling_alley', 'bus_station', 'cafe', 'campground', 'car_dealer', 'car_rental', 'car_repair', 'car_wash', 'casino', 'cemetery', 'church', 'city_hall', 'clothing_store', 'convenience_store', 'courthouse', 'dentist', 'department_store', 'doctor', 'drugstore', 'electrician', 'electronics_store', 'embassy', 'fire_station', 'florist', 'funeral_home', 'furniture_store', 'gas_station', 'gym', 'hair_care', 'hardware_store', 'hindu_temple', 'home_goods_store', 'hospital', 'insurance_agency', 'jewelry_store', 'laundry', 'lawyer', 'library', 'light_rail_station', 'liquor_store', 'local_government_office', 'locksmith', 'lodging', 'meal_delivery', 'meal_takeaway', 'mosque', 'movie_rental', 'movie_theater', 'moving_company', 'museum', 'night_club', 'painter', 'park', 'parking', 'pet_store', 'pharmacy', 'physiotherapist', 'plumber', 'police', 'post_office', 'primary_school', 'real_estate_agency', 'restaurant', 'roofing_contractor', 'rv_park', 'school', 'secondary_school', 'shoe_store', 'shopping_mall', 'spa', 'stadium', 'storage', 'store', 'subway_station', 'supermarket', 'synagogue', 'taxi_stand', 'tourist_attraction', 'train_station', 'transit_station', 'travel_agency', 'university', 'veterinary_care', 'zoo']

initial_messages = (
    {
        "role": "system",
        "content": 
            f"""
            You are an assistant for visually impaired individuals that helps users find places and directions.
            For each response, provide a conversational reply and specify an "intent" a "place" and a "type" of place (as applicable).
            When you detect that the user is interested in places, specify the "intent" as "get_places" and you will then be provided with
            a list of places with which you may discuss with the user. Once you have been provided places, do not specify "intent" as "get_places" again
            unless the user is unhappy with the current options or want a different type of place options. If the user is asking if they can submit an
            experience, the intent should be "info" and you should expect details about the experience in the following response.

            - "reply" should be the conversational response to the user's query.
            - "intent" should be "get_places" if the user wants to learn about places in the area, "info" for general information requests about places already shared, "directions" for route directions, "experience_details" for when the person is describing food or thoughts about their experience, or "get_experience" for retrieving an experience. 
            - "type" should be the type of place (such as "restaurant", "park", MUST BE from the list below), if applicable.
            - "place" should be the name of the specific location the user is interested in, if any.

            Place types: {", ".join(place_types)}
            """
    },
)

class Response(BaseModel):
    reply: str
    intent: str
    place: str
    type: str

def supply_places(places, session):
    # filter place data to the relevant fields for assistant
    data = []
    for p in places:
        if p.get('business_status') == 'OPERATIONAL':
            data.append({
                "place_id": p.get('place_id'),
                "name": p.get('name'),
                "rating": p.get('rating'),
                'opening_hours': p.get('opening_hours'),
                "types": p.get('types'),
                "user_ratings_total": p.get('user_ratings_total'),
                "vicinity": p.get('vicinity'),
            })
    session['messages'].append({"role": "system", "content": "places: " + json.dumps(data)})

def query(text, session, location=None, system=False):
    if session.get('messages') is None:
        # set default messages
        session['messages'] = list(initial_messages)

    role = "system" if system else "user"
    session['messages'].append({"role": role, "content": text})
    response = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=session['messages'],
        response_format=Response,
    )

    assistant_response = response.choices[0].message
    if assistant_response.refusal:
        return None
    session['messages'].append({"role": "assistant", "content": assistant_response.parsed.reply})
    print(assistant_response.parsed)
    if assistant_response.parsed.intent == "get_places" and not system:
        if location is None:
            raise ValueError("Location is required to get places.") # TODO: handle this more gracefully
        supply_places(get_nearby_places(location.lat, location.lng, 10000, assistant_response.parsed.type), session)
        return query("Please summarize those places, prioritizing any that seem most relevant to the kind of place the user is looking for.", session, location, system=True)
    
    return assistant_response.parsed

