from flask import Flask, session, request
from load_firebase import experiences
from text_to_speech import text_to_speech
from speech_to_text import speech_to_text
import os
from dotenv import load_dotenv
import secrets
import base64

load_dotenv()

app = Flask(__name__)
app.secret_key=os.getenv('FLASK_KEY')

# handle adding a new experience or querying for an experience
# handles all api calls
@app.route('/api', methods=['POST'])
def api():
    if 'uuid' not in session:
        # assign unique user id
        session['uuid'] = base64.b64encode(secrets.token_bytes(32).decode('utf-8'))
    if 'audio' in request and 'location' in request:
        # pass audio through speech to text
        audio_mp3_bytes = request['audio']
        text_results = speech_to_text(audio_mp3_bytes)
        if len(text_results) == 0:
            return 'We had trouble converting that audio', 400
        text_result = text_results[0] # take the most confident text result

        if session.get('enroute', False):
            # TODO: continue conversation about searching for experience
            pass
        else:
            # determine intent
            # TODO: use ChatGPT
            
            # if intent is to get directions, set session['enroute'] to True

            # TODO: store user audio and ChatGPT response
            
            # TODO: return audio to respond with

            pass


    return 'Missing audio or location in request', 400

if __name__ == '__main__':  
    app.run()