import firebase_admin
from firebase_admin import db
import os
from dotenv import load_dotenv

load_dotenv()

FIREBASE_KEY_PATH = os.getenv("FIREBASE_KEY_PATH")
FIREBASE_DB_URL = os.getenv('FIREBASE_DB_URL')

credentials_object = firebase_admin.credentials.Certificate(FIREBASE_KEY_PATH)
default_app = firebase_admin.initialize_app(credentials_object, {
    'databaseURL':FIREBASE_DB_URL
})
experiences = db.reference('experiences')