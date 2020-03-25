from flask import Flask, render_template, request, redirect
import requests
import json as json
import base64
from authorization import *

app = Flask(__name__)

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

    return render_template("callback.html")

if __name__ == "__main__":
    app.run(debug = True)
