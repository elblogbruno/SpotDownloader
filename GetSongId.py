"""
-*- coding: utf-8 -*-
"""
from os import system
import json
import sys
import requests
from urllib import *
import argparse
from urllib.parse import urlparse, urlencode, parse_qs
from urllib.request import  urlopen

YOUTUBE_SEARCH_URL = 'https://www.googleapis.com/youtube/v3/search'
YOUTUBE_VID_URL = "https://www.youtube.com/watch?v="

class YouTubeApi():

    def load_search_res(self, search_response):
        videos, channels, playlists = [], [], []
        for search_result in search_response.get("items", []):
            if search_result["id"]["kind"] == "youtube#video":
              return search_result["id"]["videoId"]
            elif search_result["id"]["kind"] == "youtube#channel":
              channels.append("{} ({})".format(search_result["snippet"]["title"],
                                           search_result["id"]["channelId"]))
            elif search_result["id"]["kind"] == "youtube#playlist":
              playlists.append("{} ({})".format(search_result["snippet"]["title"],
                                search_result["id"]["playlistId"]))

        return videos

    def search_keyword(self):
        parser = argparse.ArgumentParser()
        mxRes = 20
        parser.add_argument("--s", help="calls the search by keyword function", action='store_true')
        parser.add_argument("--r", help="define country code for search results for specific country", default="IN")
        parser.add_argument("--search", help="Search Term", default="Srce Cde")
        parser.add_argument("--max", help="number of results to return")
        parser.add_argument("--key", help="Required API key")
        parser.add_argument("--place", help="Place to save songs")
        args = parser.parse_args()

        if not args.max:
            args.max = mxRes

        if not args.key:
            exit("Please specify API key using the --key= parameter.")

        parms = {
                    'q': args.search,
                    'part': 'id,snippet',
                    'maxResults': args.max,
                    'regionCode': args.r,
                    'key': args.key
                }

        try:
            print(YOUTUBE_SEARCH_URL,parms)
            matches = self.openURL(YOUTUBE_SEARCH_URL, parms)
            print("I'm trying")

            search_response = json.loads(matches)
            i = 2

            nextPageToken = search_response.get("nextPageToken")

            songID = self.load_search_res(search_response)
            url = YOUTUBE_VID_URL + songID

            print(url)
            system("youtube-dl --extract-audio --audio-format mp3 --o '{1}.%(ext)s'  '{0}' ".format(url,args.place))
        except KeyboardInterrupt:
            print("User Aborted the Operation")

        except:
            print("Cannot Open URL at the moment.")


    def openURL(self, url, parms):
            f = urlopen(url + '?' + urlencode(parms))
            data = f.read()
            f.close()
            matches = data.decode("utf-8")
            return matches

def main():
    y = YouTubeApi()
    y.search_keyword()
    
if __name__ == '__main__':
    main()


