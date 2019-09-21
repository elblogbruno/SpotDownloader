# encoding=utf8
from os import system
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import spotipy
import spotipy.util as util


client_id = "64698e571df3463185c2e1a4433fe92b"
client_secret = "4d19dff254be41b98fe89802dcdb8a0e"
redirect_uri ="http://192.168.1.55:8888/callback"
youtube_api_key = "AIzaSyBAOr-QTMPNqYSNBvLLUOUO-PHGw8t-BqQ"

scope = 'user-library-read'

if len(sys.argv) > 3:
    username = sys.argv[1]
    playlist_url = sys.argv[2]
    playlist_split = playlist_url.split("/")
    playlist_id = playlist_split[4]
    save_location = sys.argv[3]
    print("--------------------------------------")
    print("Getting songs from this playlist url: " + playlist_url)
    print("This is the playlist id: " + playlist_id)
    print("Songs will be saved here: " + save_location)
    print("--------------------------------------")
else:
    print "Usage: %s [username] [playlist-url] [location]" % (sys.argv[0],)
    sys.exit()


def write_tracks(text_file, tracks):
    with open(text_file, 'a') as file_out:
        while True:
            for item in tracks['items']:
                if 'track' in item:
                    track = item['track']
                else:
                    track = item
                try:
                    track_url = track['external_urls']['spotify']
                    track_name = track['name'].encode('utf-8')
                    track_artist = track['artists'][0]['name']
                    search_word = track_name + " " + track_artist
                    file_out.write(track_name + " " + track_url + '\n')
                    print("--------------------------------------")
                    print("Song Name: " + track_name)
                    print("Song Artist: " + track_artist)
                    print("Song Url: " + track_url)
                    print("Search word: " + search_word)
                    print("--------------------------------------")
                    system("python3 GetSongId.py --s --search '{0}'  --max 1 --r ES --key '{1}' --place '{2}' ".format(search_word,youtube_api_key,save_location))
                except KeyError:
                    print(u'Skipping track {0} by {1} (local only?)'.format(
                            track['name'], track['artists'][0]['name']))
            # 1 page = 50 results
            # check if there are more pages
            if tracks['next']:
                tracks = spotify.next(tracks)
            else:
                break


def write_playlist(username,playlist_id):
    results = spotify.user_playlist(username, playlist_id,
                                    fields='tracks,next,name')
    text_file = u'{0}.txt'.format(results['name'], ok='-_()[]{}')
    print(u'Writing {0} tracks to {1}'.format(
            results['tracks']['total'], text_file))
    tracks = results['tracks']
    write_tracks(text_file, tracks)


token = util.prompt_for_user_token(username,scope,client_id=client_id,client_secret=client_secret,redirect_uri=redirect_uri)
spotify = spotipy.Spotify(auth=token)

# example playlist
write_playlist(username,playlist_id)
