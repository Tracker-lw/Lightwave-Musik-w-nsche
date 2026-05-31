from flask import Flask, render_template, request, jsonify
from ytmusicapi import YTMusic
import requests
import re
import time
import base64

app = Flask(__name__)
yt = YTMusic()

# 🔑 Spotify Daten
CLIENT_ID = "DEINE_CLIENT_ID"
CLIENT_SECRET = "DEIN_CLIENT_SECRET"

playlist_queue = []
skipped_songs = {}

spotify_token = None
token_expires = 0

# -----------------------------
# Spotify Token
# -----------------------------
def get_spotify_token():
    global spotify_token, token_expires

    if spotify_token and time.time() < token_expires:
        return spotify_token

    url = "https://accounts.spotify.com/api/token"
    auth = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()

    headers = {"Authorization": f"Basic {auth}"}
    data = {"grant_type": "client_credentials"}

    res = requests.post(url, headers=headers, data=data).json()

    spotify_token = res.get("access_token")
    token_expires = time.time() + res.get("expires_in", 3600)

    return spotify_token

# -----------------------------
# BPM holen
# -----------------------------
def get_bpm(title, artist):
    try:
        token = get_spotify_token()

        headers = {"Authorization": f"Bearer {token}"}

        search_url = "https://api.spotify.com/v1/search"
        params = {
            "q": f"{title} {artist}",
            "type": "track",
            "limit": 1
        }

        res = requests.get(search_url, headers=headers, params=params).json()
        items = res.get("tracks", {}).get("items", [])

        if not items:
            return 120

        track_id = items[0]["id"]

        feat_url = f"https://api.spotify.com/v1/audio-features/{track_id}"
        feat = requests.get(feat_url, headers=headers).json()

        return int(feat.get("tempo", 120))

    except:
        return 120

# -----------------------------
# Utils
# -----------------------------
def normalize_title(title):
    return re.sub(r'\(.*?\)|\[.*?\]', '', str(title)).strip().lower()

# -----------------------------
# 🔥 BPM FLOW SORT
# -----------------------------
def sort_queue():
    global playlist_queue

    if len(playlist_queue) <= 2:
        return

    # 🔒 Song 1 bleibt fix
    first_song = playlist_queue[0]

    # 🎯 Song 2 = Startpunkt
    second_song = playlist_queue[1]
    current_bpm = second_song["bpm"]

    remaining = playlist_queue[2:]

    ordered = [first_song, second_song]

    # 🔥 Flow Algorithmus
    while remaining:
        next_song = min(
            remaining,
            key=lambda s: abs(s["bpm"] - current_bpm)
        )

        ordered.append(next_song)
        remaining.remove(next_song)
        current_bpm = next_song["bpm"]

    playlist_queue = ordered

# -----------------------------
# Routes
# -----------------------------
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/display')
def display():
    return render_template('display.html')

# -----------------------------
# Search
# -----------------------------
@app.route('/search')
def search():
    query = request.args.get('q')
    if not query:
        return jsonify([])

    results = yt.search(query, filter="songs")
    songs = []

    for r in results[:12]:
        thumbs = r.get('thumbnails', [])
        cover = thumbs[-1]['url'] if thumbs else ""

        songs.append({
            "id": r.get("videoId"),
            "title": r.get("title"),
            "artist": r.get("artists", [{}])[0].get("name", "Unknown"),
            "cover": cover
        })

    return jsonify(songs)

# -----------------------------
# Add
# -----------------------------
@app.route('/add', methods=['POST'])
def add():
    global playlist_queue, skipped_songs

    data = request.json

    for song in data['songs']:
        song_id = song['id']

        # Skip-Sperre
        if song_id in skipped_songs and skipped_songs[song_id]["locked"]:
            continue

        norm = normalize_title(song['title'])

        if not any(normalize_title(s['title']) == norm for s in playlist_queue):
            song['added_at'] = time.time()
            song['bpm'] = get_bpm(song['title'], song['artist'])

            playlist_queue.append(song)

    sort_queue()

    return jsonify({"status": "ok"})

# -----------------------------
# Remove / Skip
# -----------------------------
@app.route('/remove', methods=['POST'])
def remove_song():
    global playlist_queue, skipped_songs

    data = request.json
    song_id = data.get('id')

    playlist_queue = [s for s in playlist_queue if s.get('id') != song_id]

    if song_id not in skipped_songs:
        skipped_songs[song_id] = {"skip_count": 0, "locked": True}

    skipped_songs[song_id]["skip_count"] += 1

    if skipped_songs[song_id]["skip_count"] >= 10:
        skipped_songs[song_id]["locked"] = False

    sort_queue()

    return jsonify({"status": "ok"})

# -----------------------------
# Queue
# -----------------------------
@app.route('/get_queue')
def get_queue():
    return jsonify(playlist_queue)

# -----------------------------
# Start
# -----------------------------
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)