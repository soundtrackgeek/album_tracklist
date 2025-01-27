# album_tracklist

An app to extract track list from a list of albums using the Spotify API.

## Setup

1. Install the required dependencies:

```bash
pip install -r requirements.txt
```

2. Create a `.env` file in the root directory with your Spotify API credentials:

```
SPOTIFY_CLIENT_ID='your_client_id_here'
SPOTIFY_CLIENT_SECRET='your_client_secret_here'
```

To get your Spotify API credentials:

1. Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Log in with your Spotify account
3. Create a new application
4. Copy the Client ID and Client Secret to your `.env` file

## Usage

1. Create a `list.txt` file with your albums in CSV format:

```
Album Name,Artist Name
Another Album,Another Artist
```

2. Run the script:

```bash
python main.py
```

3. The script will create an `albums.txt` file containing the track listings for each album in CSV format with the following columns:

- Album
- Artist
- Track Number
- Track Name
- Duration (ms)

## Error Handling

- If an album is not found, the script will print a message and continue with the next album
- If there's an error processing an album, the error will be printed and the script will continue with the next album
- If the Spotify credentials are missing or invalid, the script will raise an error
