from flask import Flask
from load_firebase import experiences
from text_to_speech import text_to_speech
from speech_to_text import speech_to_text

app = Flask(__name__)

# direct users to recording an experience or querying for one
@app.route('/')
def home():
    return str(experiences.get('testkey'))
    
# query for experiences
# TODO: include conversation with ChatGPT and maps API
@app.route('/query')
def query():
    return 'query!'

# record an experience
# TODO: include conversation with ChatGPT and maps API
@app.route('/record')
def record():
    return 'record!'

# tests encoding text to speech and speech to text
@app.route('/test')
def test():
    audio = text_to_speech('hi this is a test').audio_content
    text_results = speech_to_text(audio)
    print(text_results)
    return 'done'

if __name__ == '__main__':  
    app.run()