#!/usr/bin/env python3
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
import pyfiglet

###############################
# Put your own values in here #
###############################

client_id = "64698e571df3463185c2e1a4433fe92b"
client_secret = "4d19dff254be41b98fe89802dcdb8a0e"
redirect_uri ="http://192.168.1.55:8888/callback"

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
parser.add_argument('-s', '--save_location', help='Place where to save songs.')
parser.add_argument('-p', '--url', help='Spotify playlist url to get the songs from.')
parser.add_argument('-f', '--format', help='Format of the downloaded song. You can choose from aac, m4a, mp3, mp4, ogg, wav, webm. Default is .mp3', default='mp3')
args = parser.parse_args()

if not args.username:
    exit("Please write your spotify username with the -u or --username argument.")
else:
    username = args.username

if not args.save_location:
    exit("Please write your save location folder with the -s or --save_location argument.")
else:
    save_location = args.save_location
if not args.format:
    exit("Please write the format you want the song to have with the -f or --format argument. You can choose from aac, m4a, mp3, mp4, ogg, wav, webm. Default is .mp3")
else:
    song_format = args.format
if not args.username:
    exit("Please write your spotify playlist url with the -p or --url argument.")
else:
    playlist_url = args.url
    playlist_split = playlist_url.split("/")
    playlist_id = playlist_split[4]

ascii_baner = pyfiglet.figlet_format("SpotDownloader")
print(ascii_baner)

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
        print('Done downloading song in mp4, converting to {}.'.format(song_format))

def write_tracks(tracks,numOfSongs):
        i = 1
        playlist_total_lenght = 0
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
                    
                    
                    ####################################
                    #Song lenght 
                    track_lenght = track['duration_ms'] 
                    playlist_total_lenght = playlist_total_lenght + track_lenght
                    con_sec, con_min, con_hour = convertMillis(int(track_lenght))
                    if con_hour > 0:
                        clear_song_lenght =  "{0}:{1}:{2}".format(con_hour, con_min, con_sec)
                    elif con_hour == 0:
                        clear_song_lenght =  "{0}:{1}".format(con_min, con_sec)

                 
                    #####################################
                    print("--------------------------------------")
                    print("Song {0} out of {1}. Song lenght {2}".format(i,numOfSongs,clear_song_lenght) + " min")
                    print("--------------------------------------")
                    print("Song Name: " + track_name)
                    print("Song Artist: " + track_artist)
                    print("Song Url: " + track_url)
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
                            'preferredcodec': song_format,
                            'preferredquality': '192',
                        }],
                        'no-playlist': False, 
                        'quiet': args.verbose,
                        'outtmpl': '{1}{0}.%(ext)s'.format(fixed_name,save_location),                
                        'progress_hooks': [my_hook] 
                    }

                    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                        print(save_location+fixed_name+"."+song_format)
                        if os.path.exists(save_location+fixed_name+"."+ song_format):
                            print("Song already exists. Not downloading again.")
                        else:
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

        sec, mins, hour = convertMillis(int(playlist_total_lenght)) 
        print("--------------------------------------") 
        print ("I've downloaded {0} songs succesfully. {1} hours:{2} minutes:{3} seconds of music on your hands! You can check them out here {4}!".format(numOfSongs,hour,mins,sec,save_location))
        print("--------------------------------------")

def write_playlist(username,playlist_id):
    if os.path.exists(save_location):
        print("Save Location Folder exists.")
        #system("rm -R {}".format(save_location))
    else:
        print ("Save Location Folder does not exist. Creating this folder...")
        system("mkdir {}".format(save_location))

    results = spotify.user_playlist(username, playlist_id,
                                    fields='tracks,next,name')
    
    print(u'Getting {0} tracks from {1}'.format(
            results['tracks']['total'], results['name']))
    tracks = results['tracks']
    write_tracks(tracks,results['tracks']['total'])


token = util.prompt_for_user_token(username,scope,client_id=client_id,client_secret=client_secret,redirect_uri=redirect_uri)
spotify = spotipy.Spotify(auth=token)

write_playlist(username,playlist_id)
