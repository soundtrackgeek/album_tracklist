import csv
import requests
import base64
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Spotify API credentials from environment variables
CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')

# Get access token
def get_spotify_token():
    auth_string = f"{CLIENT_ID}:{CLIENT_SECRET}"
    auth_bytes = auth_string.encode('utf-8')
    auth_base64 = str(base64.b64encode(auth_bytes), 'utf-8')

    url = 'https://accounts.spotify.com/api/token'
    headers = {
        'Authorization': f'Basic {auth_base64}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {'grant_type': 'client_credentials'}
    
    response = requests.post(url, headers=headers, data=data)
    response.raise_for_status()
    return response.json()['access_token']

# Search for album and get tracks
def get_album_tracks(album_name, artist_name, token):
    headers = {'Authorization': f'Bearer {token}'}
    
    # Search for album
    search_url = 'https://api.spotify.com/v1/search'
    query = f"album:{album_name} artist:{artist_name}"
    params = {
        'q': query,
        'type': 'album',
        'limit': 1
    }
    
    search_response = requests.get(search_url, headers=headers, params=params)
    search_response.raise_for_status()
    albums = search_response.json()['albums']['items']
    
    if not albums:
        return None
    
    # Get album ID from first result
    album_id = albums[0]['id']
    
    # Get tracks
    tracks_url = f'https://api.spotify.com/v1/albums/{album_id}/tracks'
    tracks_response = requests.get(tracks_url, headers=headers)
    tracks_response.raise_for_status()
    
    return tracks_response.json()['items']

# Main script
def main():
    # Check if environment variables are set
    if not CLIENT_ID or not CLIENT_SECRET:
        raise ValueError("Missing Spotify API credentials. Please check your .env file.")

    token = get_spotify_token()
    
    with open('list.txt', 'r', encoding='utf-8') as infile, \
         open('albums.txt', 'w', newline='', encoding='utf-8') as outfile:
        
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        writer.writerow(['Album', 'Artist', 'Track Number', 'Track Name', 'Duration (ms)'])
        
        for row in reader:
            if len(row) < 2:
                continue
            
            album_name, artist_name = row[0].strip(), row[1].strip()
            print(f"Processing {album_name} by {artist_name}...")
            
            try:
                tracks = get_album_tracks(album_name, artist_name, token)
                if not tracks:
                    print(f"Album not found: {album_name}")
                    continue
                
                for track in tracks:
                    writer.writerow([
                        album_name,
                        artist_name,
                        track['track_number'],
                        track['name'],
                        track['duration_ms']
                    ])
                
            except Exception as e:
                print(f"Error processing {album_name}: {str(e)}")

if __name__ == '__main__':
    main()