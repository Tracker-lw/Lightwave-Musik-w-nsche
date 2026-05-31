# Lightwave-Musik-wünsche
A web-based party playlist system that allows guests to search for songs, submit requests from their phones, and automatically organize the playlist using BPM-based flow optimization.

Features
🎵 Song search via YouTube Music
📱 Mobile-friendly interface
➕ Guests can add songs directly to the queue
🎯 Automatic BPM detection using Spotify Audio Features
🔄 Intelligent playlist sorting based on BPM similarity
📈 Smooth musical flow between songs
🔒 First song remains fixed
🎚️ Second song defines the BPM direction
🚫 Duplicate song protection
⏭️ Song removal system
🔐 Skip-lock system for recently removed songs
☑️ Interactive playlist management
🔄 Automatic live updates
How It Works
Guests search for a song using the web interface.
The song is added to the queue.
The system retrieves the song BPM from Spotify.
The playlist is automatically reordered to minimize BPM differences between consecutive songs.
The display page updates automatically and shows the current playlist.
BPM Flow Optimization

The playlist is optimized to create smooth transitions:

The first song stays fixed.
The second song is used as the BPM reference point.
All following songs are reordered automatically.
The algorithm always selects the song with the smallest BPM difference to the currently playing song.

This creates a natural and DJ-like progression through the playlist.

Technologies Used
Backend
Python
Flask
Requests
YouTube Music API (ytmusicapi)
Spotify Web API
Frontend
HTML5
CSS3
JavaScript (Vanilla JS)
API Endpoints
Endpoint	Method	Description
/search	GET	Search songs via YouTube Music
/add	POST	Add songs to the playlist
/remove	POST	Remove songs from the playlist
/get_queue	GET	Retrieve current playlist
/display	GET	Playlist display page
Installation
git clone https://github.com/yourusername/party-playlist-system.git

cd party-playlist-system

pip install flask ytmusicapi requests

Add your Spotify API credentials in app.py:

CLIENT_ID = "YOUR_SPOTIFY_CLIENT_ID"
CLIENT_SECRET = "YOUR_SPOTIFY_CLIENT_SECRET"

Start the server:
python app.py

Open:
http://localhost:5000

Display page:
http://localhost:5000/display

Future Improvements:
- Spotify playback integration
- Song voting system
- Multiple playlists/events
- User authentication
- SQLite/PostgreSQL database support
- WebSocket real-time updates
- Advanced DJ transition algorithms
- Playlist export

License:
This project is released under the MIT License.
