from firebase import firebase
from flask import Flask
import os
from dotenv import load_dotenv

load_dotenv()

FIREBASE_KEY = os.getenv("FIREBASE_KEY")

firebase = firebase.FirebaseApplication(FIREBASE_KEY, None)

app = Flask(__name__)

# direct users to recording an experience or querying for one
@app.route('/')
def home():
    experiences = firebase.get('/experiences', None)
    return str(experiences)
    
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

if __name__ == '__main__':  
   app.run()