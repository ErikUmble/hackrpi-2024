from flask import Flask
from load_firebase import experiences

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

if __name__ == '__main__':  
   app.run()