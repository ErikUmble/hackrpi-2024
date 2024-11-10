import firebase_admin
from firebase_admin import db
import os
from dotenv import load_dotenv
import base64

load_dotenv()

FIREBASE_KEY_PATH = os.getenv("FIREBASE_KEY_PATH")
FIREBASE_DB_URL = os.getenv('FIREBASE_DB_URL')

credentials_object = firebase_admin.credentials.Certificate(FIREBASE_KEY_PATH)
default_app = firebase_admin.initialize_app(credentials_object, {
    'databaseURL':FIREBASE_DB_URL
})
experiences = db.reference('experiences')

# submit an experience
def submit_experience(original_audio, transcribed, location):
    if location is None:
        return
    experiences.push(
        {
            'audio': base64.b64encode(original_audio).decode('utf8'),
            'transcription': transcribed,
            'location': location,
        }
    )

def get_experiences(location):
    if location is None:
        return None
    results = list(experiences.order_by_child('location').equal_to(location).get().values())
    for index in range(len(results)):
        results[index]['audio'] = base64.b64decode(results[index]['audio'])
    return results