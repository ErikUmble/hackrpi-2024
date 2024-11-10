from flask import (
    Flask,
    session,
    request,
    send_from_directory,
    make_response,
)
from text_to_speech import text_to_speech
from speech_to_text import speech_to_text
import os
from dotenv import load_dotenv
import secrets
import base64
from maps import Location, get_matching_place
from assistant import query
import firebase_db
import random

load_dotenv()

app = Flask(__name__, static_folder='../frontend/dist/spa')
app.secret_key=os.getenv('FLASK_KEY')

# serve Quasar frontend
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_frontend(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        # Serve static files for the frontend
        return send_from_directory(app.static_folder, path)
    else:
        # Serve index.html for all other routes (Single Page App)
        return send_from_directory(app.static_folder, "index.html")

# handle adding a new experience or querying for an experience
# handles all api calls
@app.route('/api', methods=['POST'])
def api():
    if 'uuid' not in session:
        # assign unique user id
        session['uuid'] = base64.b64encode(secrets.token_bytes(32))
    if 'audio' in request.files and 'longitude' in request.form and 'latitude' in request.form:
        # pass audio through speech to text
        audio_wav_file = request.files['audio']
        audio_wav_bytes = audio_wav_file.read()
        text_results = speech_to_text(audio_wav_bytes)
        if len(text_results) == 0:
            return 'We had trouble converting that audio', 400
        text_transcript = ''.join([result.alternatives[0].transcript for result in text_results]) # take the most confident text result
        print(text_results)
        print(text_transcript)
        location = Location(request.form['latitude'], request.form['longitude'])

        '''
        # for testing, convert text back into audio and return
        audio_response = text_to_speech(text_transcript)
        return make_response(audio_response)
        '''
            
        if session.get('enroute', False):
            session['enroute'] = False
            return make_response(text_to_speech("I'm sorry, I still need to look up the route."))
            # TODO: continue conversation about searching for experience
            pass
        else:
            response = query(text_transcript, session, location)

            # if intent is to get directions, set session['enroute'] to True
            if response.intent == "get_experience":
                experiences = firebase_db.get_experiences(get_matching_place(lat=location.lat, lng=location.lng, query=response.place))
                # for now, choose a random experience to share
                if experiences is None or len(experiences) == 0:
                    return make_response(text_to_speech('Sorry, we do not have any experiences for that location yet'))
                # TODO: have a better way to choose
                chosen_experience = random.choice(experiences)
                return make_response(chosen_experience['audio'])
            else:
                if response.intent == "directions":
                    session['enroute'] = True
                    # TODO: get directions
                elif response.intent == "experience_details":
                    firebase_db.submit_experience(
                        audio_wav_bytes,
                        text_transcript,
                        get_matching_place(lat=location.lat, lng=location.lng, query=response.place)
                    )
                return make_response(text_to_speech(response.reply))

    return 'Missing audio or location in request', 400


if __name__ == '__main__':  
    app.run(debug=True)