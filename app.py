from flask import Flask, render_template, request, redirect
import requests
import json as json
from flask_bootstrap import Bootstrap
from authorization import *

app = Flask(__name__)
Bootstrap(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods = ["GET", "POST"])
def login():
    query = "https://accounts.spotify.com/authorize?client_id={}&response_type=code&redirect_uri=http://localhost:5000/callback".format(client_id)
    return redirect(query)

@app.route("/callback", methods = ["GET", "POST"])
def callback():
    code = request.args.get("code")
    print(code)
    print(encoded)
    request_body = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": "http://localhost:5000/callback"
    }
    query = "https://accounts.spotify.com/api/token"
    response = requests.post(
        query,
        data = request_body,
        headers = {
            "Authorization": "Basic " + encoded
        }
    )
    response_json = response.json()
    print("---------------------------------------------")
    print(response_json["access_token"])
    print("---------------------------------------------")
    print(response_json)

    query0 = "https://api.spotify.com/v1/me"
    response0 = requests.get(
        query0,
        headers = {
            "Authorization": "Bearer {}".format(response_json["access_token"])
        }
    )
    response_json0 = response0.json()
    print("")
    print(response_json0)

    query1 = "https://api.spotify.com/v1/me/playlists?limit=50"
    response1 = requests.get(
        query1,
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(response_json["access_token"])
        }
    )
    response_json1 = response1.json()
    print(response.status_code)
    #playlists = response_json["items"][]["name"]
    playlists_items = []
    for playlists in response_json1["items"]:
        playlists_items.append(playlists)
        #print(playlists)

    playlists_names = []
    for playlist in playlists_items:
        playlists_names.append(playlist["name"])
        print(playlist["name"])

    return render_template("callback.html", json_obj = response_json0, liste = playlists_names)

if __name__ == "__main__":
    app.run(debug = True)
