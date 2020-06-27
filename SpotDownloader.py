# encoding=utf8
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import youtube_dl
import argparse
import pyfiglet
import os

import json
from os_helper import (dirname, try_create_lock_file,
                           try_delete_lock_file,mkdir,isdir)

#############################
# DO NOT MODIFY THIS VALUES #
#############################
current_track = " "
search_word = " "
#############################

def get_arguments():
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument('-v', '--verbose', action='store_false', help='Display more information on downloader.',default = True)
    parser.add_argument('-o', '--overwrite', action='store_true', help='If given path has got songs, deletes the folder with already downloaded songs.',default = False)
    parser.add_argument('-u', '--username', help='Spotify Username.')
    parser.add_argument('-s', '--save_location', help='Place where to save songs.')
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
    return args

class SpotDownloader(object):
    def __init__(self, args):

        """ Spotify API Constructor
        :param client_id: client id provided by Spotify
        :param client_secret: client secret provided by Spotify
        :param redirect_uri: redirect uri provided by Spotify
        :param sp: spotipy API handler.
        """
        self.save_location = args.save_location
        self.song_format = args.format
        self.overwrite = args.overwrite
        self.verbose  = args.verbose
        self.username = args.username
        self.scope = "playlist-read-private" 

        with open('keys.json') as json_file:
            data = json.load(json_file)
            self.client_id = data['SPOTIPY_CLIENT_ID']
            self.client_secret = data['SPOTIPY_CLIENT_SECRET']
            self.redirect_uri = data['SPOTIPY_REDIRECT_URI']
            self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=self.scope, username=self.username,client_id=self.client_id,client_secret=self.client_secret,redirect_uri=self.redirect_uri))

    def show_tracks(results):
        for i, item in enumerate(results['items']):
            track = item['track']
            print(
                "   %d %32.32s %s" %
                (i, track['artists'][0]['name'], track['name']))

    def make_list_with_fixed_names(self,results):
        songDic = {}
        list_of_songs = []
        for i, item in enumerate(results['items']):
            track = item['track']
            try:
                track_url = track['external_urls']['spotify']
                track_name = track['name'].encode('utf-8')
                track_artist = track['artists'][0]['name'].encode('utf-8')
                track_lenght = track['duration_ms'] 

                search_word = track_name + " " + track_artist 
                  
                fixed_name = " "
                
                if "/" in search_word:
                    fixed_name = search_word.replace("/","-")
                    if args.verbose == False:
                        print("Fixing song name format...")
                else:
                    fixed_name = search_word
                    if args.verbose == False:
                        print("Song name is correct.")

                songPlace = self.save_location+search_word+"."+self.song_format
                songDic = {
                    "name": track_name,
                    "artist": track_artist,
                    "url": track_url,
                    "search_word": fixed_name,
                    "lenght": track_lenght,
                    "song_path": songPlace
                }

                list_of_songs.append(songDic)
            except KeyError:
                        print(u'Skipping track {0} by {1} (local only?)'.format(tracks['name'], tracks['artists']))
        print("Fixed all names on the playlist tracks!")
        return list_of_songs

    def convertMillis(self,millis):
        seconds=(millis/1000)%60
        minutes=(millis/(1000*60))%60
        hours=(millis/(1000*60*60))%24
        return seconds, minutes, hours
    def my_hook(self,d):
        if d['status'] == 'downloading':
            folder_path = dirname(d['filename'])
            try_create_lock_file(folder_path)
        if d['status'] == 'finished':
            print('Done downloading song in mp4, converting to {}.'.format(self.song_format))

    def write_tracks(self,results):
        num_of_songs = len(results)
        playlist_total_lenght = 0
        for i, track in enumerate(results):
            try:
                ####################################
                #Main Song values.
                track_url = track['url']
                track_name = track['name']
                track_artist = track['artist']
                search_word = track['search_word']               
                song_path = track['song_path']
                ####################################
                #Song lenght. 
                track_lenght = track['lenght'] 
                playlist_total_lenght = playlist_total_lenght + track_lenght
                con_sec, con_min, con_hour = self.convertMillis(int(track_lenght))
                if con_hour > 0:
                    clear_song_lenght =  "{0}:{1}:{2}".format(con_hour, con_min, con_sec)
                elif con_hour == 0:
                    clear_song_lenght =  "{0}:{1}".format(con_min, con_sec)

                
                #####################################
                print("--------------------------------------")
                print("Song {0} out of {1}. Song lenght {2}".format(i+1,num_of_songs,clear_song_lenght) + " min")
                print("--------------------------------------")
                print("Song Name: " + track_name)
                print("Song Artist: " + track_artist)
                print("Song Url: " + track_url)
                print("Search word: " + search_word)
                print("--------------------------------------")

                ydl_opts = {
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': self.song_format,
                        'preferredquality': '192',
                    }],
                    'writethumbnail': False,
                    'writeinfojson': False,
                    'no-playlist': False, 
                    'quiet': self.verbose,
                    'outtmpl': '{1}{0}.%(ext)s'.format(search_word,self.save_location),                
                    'progress_hooks': [self.my_hook] 
                }

                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    if os.path.exists(song_path):
                        print("Song already exists on the given path. Not downloading again.")
                    else:
                        try:
                            ydl.download(["ytsearch:'{0}'".format(search_word)])
                        except youtube_dl.utils.DownloadError as e:
                            print e
                        finally:
                            try_delete_lock_file(search_word+self.save_location)
            except KeyError:
                print(u'Skipping track {0} by {1} (local only?)'.format(
                        track['name'], track['artists']))
        else:
            sec, mins, hour = self.convertMillis(int(playlist_total_lenght)) 

            print("--------------------------------------") 
            print ("I've downloaded {0} songs succesfully. {1} hours:{2} minutes:{3} seconds of music on your hands! You can check them out here {4}!".format(num_of_songs,hour,mins,sec,self.save_location))
            print("--------------------------------------")
        
    def choose_playlist(self):
        playlists = self.sp.current_user_playlists()

        playlist_list = []
        playlist_id = []

        i = 1
        print("These are your playlist, please choose one: ")

        for playlist in playlists['items']:
            print("{0}) {1}".format(i,playlist['name'].encode('utf8')))
            playlist_list.append(playlist['name'])
            playlist_id.append(playlist['id'])
            i=i+1

        playlist_index = input("Choose a playlist by the number (if you want to download a custom one write 0): ")
        while playlist_index < 0 or playlist_index > len(playlist_list):
            print(playlist_index)
            print("Choose a playlist available on the list.")
            playlist_index = input("Choose a playlist by the number (if you want to download a custom one write 0): ")

        if playlist_index == 0:
            final_id = raw_input("Paste the url of the playlist: ")
        else:
            final_id = playlist_id[playlist_index-1]
        
        print ("Gonna download all the songs from this playlist {0}".format(playlist_list[playlist_index-1]))
        
        return final_id

    def check_save_folder(self):
        print("Checking save folder {0}...".format(self.save_location))
        if self.save_location[-1] != "/":
            self.save_location = self.save_location+"/" #fixes if there is no / at the end of the save location path.
        
        if isdir(self.save_location):
            print("Save Location Folder exists.")
            if self.overwrite:
                print("Overwriting folder...")
                os.system("sudo rm -R {}".format(self.save_location))
            else:
                print("Not Overwriting folder...")
        else:
            print ("Save Location Folder does not exist. Creating this folder...")
            mkdir(self.save_location)
    
    def welcome_message(self):
        ascii_baner = pyfiglet.figlet_format("SpotDownloader")
        print(ascii_baner)
        print("--------------------------------------")
        print("Getting playlists from this username: " + self.username)
        print("Songs will be saved here: " + self.save_location)
        print("--------------------------------------")
    
    def download_songs(self):
        self.welcome_message()

        self.check_save_folder()

        self.playlist_id = self.choose_playlist()

        results = self.sp.playlist(self.playlist_id, fields="tracks,next")

        tracks = results['tracks']    

        tracks_list = self.make_list_with_fixed_names(tracks)

        self.write_tracks(tracks_list)



if __name__ == "__main__":
    args = get_arguments()
    sp = SpotDownloader(args)
    sp.download_songs()