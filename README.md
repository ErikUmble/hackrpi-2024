## Able
Able is voice-based interactive map & assistant for individuals with vision impairment. 
Ask about the places nearby and hear experiences from other community members (in their recorded voice).
Motivate and encourage each other to keep exploring and enjoying the city in spite of vision difficulties. 
Use your native language and hear results and experiences in that language.

Try it [here](https://ablemap.tech/).

## HackRPI 2024
HackRPI is RPI's annual hackathon. Participants form teams up to 4 people and spend up to 24 hours 
creating apps, websites, games, and more to solve real problems. This year's category was Urban Upgrades,
with a theme of improving urban life. We created Able to make the city more accessible to individuals with
vision impairment, and won the Accessiblity prize track.

## Contributors 
Joel McCandless & Erik Umble

## Hosting
Able works by tying together a bunch of incredible APIs. We're standing on the shoulders of giants to create
something like this in just 24 hours. As such, if you would like to host an instance of Able yourself, you
are going to need to get an API key from OpenAI, Google Maps, Firebase Admin, Google Speech-to-Text, and Google
Speech (for text to speech).

Clone this repository.

Create a `.env` file in the root directory with the following format:
```
MAPS_API_KEY=<Your Google Maps key>
FIREBASE_KEY_PATH=<JSON filename>
GOOGLE_APPLICATION_CREDENTIALS=<JSON filename>
FIREBASE_DB_URL=<Your Firebase db url>
OPENAI_API_KEY=<Your OpenAI key>
FLASK_KEY=<long random key>
```
We used a Google Cloud project with service accounts which have roles (permissions) enabling them to use
Firebase Admin, Google Speech-to-Text, and Google Speech. Service agents authenticate via a .json credentials
file. If you also use a Google Cloud Project, you'll need to share the path to your credentials
files in the `.env` file where we indicate `<JSON filename>`. You also need to update `Dockerfile` and
`docker-compose.yml` with your GOOGLE_APPLICATION_CREDENTIALS filepath and Firebase credentials path.
Note that you need to configure the Google Maps key to enable Places Search and Text Search. Firebase and
Google Application Credentials are best kept in their provided JSON files, and pointed to by this `.env`.
If you choose not to use a Google Cloud project, you'll be authenticating to the Google Cloud API in a
different way and may not need the Google and Firebase json files.

Now you can run
```bash
source run.sh
```
or 
```bash
docker compose build
docker compose up
```
to spin up Flask on localhost. You can test the app this way, but it likely won't be accessible 
to other devices yet. You need a webserver (such as nginx) to proxy connections from port 80/443 to Flask.

Since Able requires microphone and location access, your users must connect over https for browsers such
as Chrome or Edge to allow those permissions at all. If you don't have SSL certificates for your domain yet,
we recommend following the instructions from [letsencrypt](https://letsencrypt.org/). 

To proxy connections to Flask, you will need to add something like the following to the nginx conf file
your server is using.
```
# /etc/nginx/sites-available/default
...
server {
    server_name your_domain;
    location / {
        proxy_pass http://localhost:9000;
    }

    # Certbot managed area
}
```