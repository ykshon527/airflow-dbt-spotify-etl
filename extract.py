import base64
import requests
import datetime
import pandas as pd
import urllib.parse
import http.server
import socketserver
import threading
import webbrowser
import time

CLIENT_ID = "4d8ff6e2a8e44860a78e82dd62fe00e0"
CLIENT_SECRET = "109a57119b3e4c6aa8fd236dde26dca3"
REDIRECT_URI = "http://127.0.0.1:8080/callback"
SCOPE = "user-read-recently-played"

auth_code = None

# HTTP handler to catch redirect with the authorization code
class OAuthHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        global auth_code
        params = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        if "code" in params:
            auth_code = params["code"][0]
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(b"You can close this window.")
        else:
            self.send_response(400)
            self.end_headers()

def start_http_server():
    with socketserver.TCPServer(("127.0.0.1", 8080), OAuthHandler) as httpd:
        httpd.handle_request()

def get_access_token():
    global auth_code
    auth_code = None

    # Step 1: Ask user to log in and approve
    params = {
        "client_id": CLIENT_ID,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "scope": SCOPE
    }
    auth_url = "https://accounts.spotify.com/authorize?" + urllib.parse.urlencode(params)

    # Start temporary local server in background
    threading.Thread(target=start_http_server, daemon=True).start()

    print("Opening browser for Spotify login...")
    webbrowser.open(auth_url)

    # Wait for redirect to set auth_code
    while auth_code is None:
        time.sleep(0.1)

    # Step 2: Exchange code for access token
    token_url = "https://accounts.spotify.com/api/token"
    auth_str = f"{CLIENT_ID}:{CLIENT_SECRET}"
    b64_auth_str = base64.b64encode(auth_str.encode()).decode()

    headers = {
        "Authorization": f"Basic {b64_auth_str}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "authorization_code",
        "code": auth_code,
        "redirect_uri": REDIRECT_URI
    }

    response = requests.post(token_url, headers=headers, data=data)
    response.raise_for_status()
    token = response.json().get("access_token")

    print("Access Token:", token)
    return token

# Creating an function to be used in other pyrhon files
def return_dataframe(spotify_token): 
    input_variables = {
        "Accept" : "application/json",
        "Content-Type" : "application/json",
        "Authorization" : "Bearer {token}".format(token=spotify_token)
    }
     
    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(days=7)
    yesterday_unix_timestamp = int(yesterday.timestamp()) * 100

    # Download all songs you've listened to "after yesterday", which means in the last 24 hours      
    r = requests.get("https://api.spotify.com/v1/me/player/recently-played?after={time}".format(time=yesterday_unix_timestamp), headers = input_variables)
    print(r)

    data = r.json()
    song_names = []
    artist_names = []
    played_at_list = []
    timestamps = []

    # Extracting only the relevant bits of data from the json object      
    for song in data["items"]:
        song_names.append(song["track"]["name"])
        artist_names.append(song["track"]["album"]["artists"][0]["name"])
        played_at_list.append(song["played_at"])
        timestamps.append(song["played_at"][0:10])
        
    # Prepare a dictionary in order to turn it into a pandas dataframe below       
    song_dict = {
        "song_name" : song_names,
        "artist_name": artist_names,
        "played_at" : played_at_list,
        "timestamp" : timestamps
    }
    song_df = pd.DataFrame(song_dict, columns = ["song_name", "artist_name", "played_at", "timestamp"])
    return song_df

# if __name__ == "__main__":
#     #token = get_access_token()
#     df = return_dataframe('')
