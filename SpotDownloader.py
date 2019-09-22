# encoding=utf8
from __future__ import unicode_literals
import os
from os import system
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import spotipy
import spotipy.util as util
import youtube_dl
import argparse

###############################
# Put your own values in here #
###############################

client_id = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
client_secret = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
redirect_uri ="XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

#############################
# DO NOT MODIFY THIS VALUES #
#############################
current_track = " "
search_word = " "
scope = 'user-library-read'
#############################

parser = argparse.ArgumentParser(add_help=True)
parser.add_argument('-v', '--verbose', action='store_false', help='Display more information on downloader.')
parser.add_argument('-u', '--username', help='Spotify Username.')
parser.add_argument('-s', '--save_location', help='Place where to save songs. Default folder is ~/mp3/', default= '~/mp3/')
parser.add_argument('-p', '--url', help='Spotify playlist url to get the songs from.')

args = parser.parse_args()

username = args.username
save_location = args.save_location

playlist_url = args.url
playlist_split = playlist_url.split("/")
playlist_id = playlist_split[4]

print("--------------------------------------")
print("Getting songs from this playlist url: " + playlist_url)
print("This is the playlist id: " + playlist_id)
print("Songs will be saved here: " + save_location)
print("--------------------------------------")


def convertMillis(millis):
     seconds=(millis/1000)%60
     minutes=(millis/(1000*60))%60
     hours=(millis/(1000*60*60))%24
     return seconds, minutes, hours

def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading song in mp4, converting to .mp3')

def write_tracks(text_file, tracks,numOfSongs):
    with open(text_file, 'a') as file_out:
        i = 1
        playlist_total_lenght = " "
        while i < numOfSongs:
            for item in tracks['items']:
                current_track = item
                if 'track' in item:
                    track = item['track']
                else:
                    track = item
                try:
                    track_url = track['external_urls']['spotify']
                    track_name = track['name'].encode('utf-8')
                    track_artist = track['artists'][0]['name']

                    search_word = track_name + " " + track_artist                   
                    file_out.write(track_name + " " + track_url + '\n') #Writing into file.
                    
                    ####################################
                    #Song lenght 
                    track_lenght = track['duration_ms'] 
                    con_sec, con_min, con_hour = convertMillis(int(track_lenght))
                    if con_hour > 0:
                        clear_song_lenght =  "{0}:{1}:{2}".format(con_hour, con_min, con_sec)
                    elif con_hour == 0:
                        clear_song_lenght =  "{0}:{1}".format(con_min, con_sec)
                    playlist_total_lenght = playlist_total_lenght + clear_song_lenght
                    #####################################
                    print("--------------------------------------")
                    print("Song {0} out of {1}. Playlist lenght {2}".format(i,numOfSongs,playlist_total_lenght))
                    print("--------------------------------------")
                    print("Song Name: " + track_name)
                    print("Song Artist: " + track_artist)
                    print("Song Url: " + track_url)
                    print("Song Lenght: " + clear_song_lenght + " min")
                    print("Search word: " + search_word)
                    print("--------------------------------------")

                    fixed_name = " "
                    if "/" in search_word:
                        fixed_name = search_word.replace("/","-")
                        print("Fixing song name format...")
                    else:
                        fixed_name = search_word
                        print("Song name is correct.")

                    ydl_opts = {
                        'format': 'bestaudio/best',
                        'postprocessors': [{
                            'key': 'FFmpegExtractAudio',
                            'preferredcodec': 'mp3',
                            'preferredquality': '192',
                        }],
                        'no-playlist': False, 
                        'quiet': args.verbose,
                        'outtmpl': '{1}{0}.%(ext)s'.format(fixed_name,save_location),                
                        'progress_hooks': [my_hook] 
                    }

                    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                        ydl.download(["ytsearch:'{0}'".format(search_word)])
                        i = i + 1
                except KeyError:
                    print(u'Skipping track {0} by {1} (local only?)'.format(
                            track['name'], track['artists'][0]['name']))
            # 1 page = 50 results
            # check if there are more pages
            if tracks['next']:
                tracks = spotify.next(tracks)
            else:
                break
        print("--------------------------------------")
        print ("I've downloaded {0} songs succesfully. You can check them out here {1} !".format(numOfSongs,save_location))
        print("--------------------------------------")

def write_playlist(username,playlist_id):
    if os.path.isdir(save_location):
        print("Save Location Folder exists.")
        #system("rm -R {}".format(save_location))
    else:
        print ("Save Location Folder does not exist. Creating this folder...")
        system("mkdir {}".format(save_location))

    results = spotify.user_playlist(username, playlist_id,
                                    fields='tracks,next,name')
    text_file = u'{0}.txt'.format(results['name'], ok='-_()[]{}')
    print(u'Writing {0} tracks to {1}'.format(
            results['tracks']['total'], text_file))
    tracks = results['tracks']
    write_tracks(text_file, tracks,results['tracks']['total'])


token = util.prompt_for_user_token(username,scope,client_id=client_id,client_secret=client_secret,redirect_uri=redirect_uri)
spotify = spotipy.Spotify(auth=token)

write_playlist(username,playlist_id)
