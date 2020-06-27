import os
import argparse
from spotdownloader.SpotDownloader import SpotDownloader


def main(args=None):
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
    Sptd = SpotDownloader(args,'keys.json')
    Sptd.download_songs()


if __name__ == "__main__":
    main()