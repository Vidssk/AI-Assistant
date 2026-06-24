import spotipy
from spotipy.oauth2 import SpotifyOAuth
from config.config import spotify_credentials, APP_MAP
import subprocess
import time

class MusicManager:

    def __init__(self):
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=spotify_credentials["client_id"],
            client_secret=spotify_credentials["client_secret"],
            redirect_uri=spotify_credentials["redirect_uri"],
            scope=(
            "user-library-read "
            "user-modify-playback-state "
            "user-read-playback-state"
            )
        ))

        self.SPOTIFY_DEVICE_ID = spotify_credentials["SPOTIFY_DEVICE_ID"]

    def play(self, query):
        path = APP_MAP.get("spotify")
        subprocess.Popen(path, creationflags=subprocess.CREATE_NO_WINDOW)
        time.sleep(2)
        print(f"Playing: {query}")

        track_uri = self.search_song(query)

        if not track_uri:
            print("Song not found.")
            return

        try:
            self.sp.start_playback(
                uris=[track_uri],
                device_id=self.SPOTIFY_DEVICE_ID
            )

            print("Playback started.")

        except Exception as e:
            print(f"Error starting playback: {e}")

    def pause(self):
        try:
            self.sp.pause_playback()
            print("Music paused.")

        except Exception as e:
            print(f"Error pausing playback: {e}")

    def resume(self):
        try:
            self.sp.start_playback()
            print("Music resumed.")

        except Exception as e:
            print(f"Error resuming playback: {e}")

    def next_track(self):
        try:
            self.sp.next_track()
            print("Skipped to next track.")

        except Exception as e:
            print(f"Error skipping track: {e}")


    def previous_track(self):
        try:
            self.sp.previous_track()
            print("Returned to previous track.")

        except Exception as e:
            print(f"Error going to previous track: {e}")

    def set_volume(self, volume):
        try:
            self.sp.volume(volume)
            print(f"Volume set to {volume}%")

        except Exception as e:
            print(f"Error setting volume: {e}")


    def search_song(self, query):
        print(f"Searching for: {query}")

        results = self.sp.search(
            q=query,
            type="track",
            limit=1
        )

        tracks = results.get("tracks", {}).get("items", [])

        if not tracks:
            return None

        track = tracks[0]

        print(
            f"Found: {track['name']} "
            f"by {track['artists'][0]['name']}"
        )

        return track["uri"]
    def list_devices(self):
        devices = self.sp.devices()

        for device in devices.get("devices", []):
            print(
                f"{device['name']} "
                f"(active={device['is_active']})"
                f"(id ={device['id']})"
            )

        return devices

if __name__ == "__main__":
    music_manager = MusicManager()
    print(music_manager.sp.current_user()["display_name"])
    music_manager.list_devices()
    music_manager.play("all of me")
    # music_manager.pause()