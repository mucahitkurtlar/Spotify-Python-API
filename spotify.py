import json
import requests

from authorization import spotify_auth_token, spotify_user_id
#from playlist import playlist_id

class Spotify:
    def create_playlist(self):
        request_body = json.dumps({
            "name": "Spotify API",
            "description": "Automated Task Test",
            "public": True
        })
        query = "https://api.spotify.com/v1/users/{}/playlists".format(spotify_user_id)
        response = requests.post(
            query,
            data = request_body,
            headers = {
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(spotify_auth_token)
            }
        )
        response_json = response.json()
        print(response.status_code)
        return response_json["id"]

    def get_track(self, artist_name, track_name):
        query = "https://api.spotify.com/v1/search?query=track%3A{}+artist%3A{}&type=track&offset=0&limit=20".format(track_name, artist_name)
        response = requests.get(
            query,
            headers = {
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(spotify_auth_token)
            }
        )
        response_json = response.json()
        songs = response_json["tracks"]["items"]

        # only use the first song
        uri = songs[0]["uri"]

        return uri

    def get_list_of_playlists(self):
        query = "https://api.spotify.com/v1/me/playlists?limit=50"
        response = requests.get(
            query,
            headers = {
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(spotify_auth_token)
            }
        )
        response_json = response.json()
        print(response.status_code)
        #playlists = response_json["items"][]["name"]
        playlists_items = []
        for playlists in response_json["items"]:
            playlists_items.append(playlists)
            #print(playlists)

        playlists_names = []
        for playlist in playlists_items:
            playlists_names.append(playlist["name"])
            print(playlist["name"])

        return playlists_names

    def add_track_to_playlist(self, artist_name, track_name):
        playlist_id = self.create_playlist()
        print("Playlist id: ", playlist_id)
        track_uri = [self.get_track(artist_name, track_name)]
        print("Track URI: ", track_uri)
        request_data = json.dumps(track_uri)
        query = "https://api.spotify.com/v1/playlists/{}/tracks".format(playlist_id)
        response = requests.post(
            query,
            data = request_data,
            headers = {
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(spotify_auth_token)
            }
        )
        print(response.status_code)
        response_json = response.json()
        return response_json


if __name__ == "__main__":
    spotify = Spotify()
    spotify.get_list_of_playlists()
    #spotify.add_track_to_playlist("Rammstein", "Küss mich (Fellfrosch)")
