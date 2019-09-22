# SpotDownloader
This a sample and easy to use app in python that downloads all you music in .MP3 from a given spotify playlist!
Simply pass your username , playlist url , and get all your songs in high quality .MP3!

## How to install
To install the program, fire up your linux or windows distributed machine and run this command.

```
wget https://raw.githubusercontent.com/elblogbruno/SpotDownloader/master/setup.sh && sudo sh setup.sh
```
That's it.

The installation script will:
- Download SpotDownloader and install the necessary dependencies

## Configuration of the downloader. 
Change values inside SpotDownloader.py with your spotify account credentials. You can get your credentials from here:
https://developer.spotify.com/my-applications/#!/applications

![alt text](https://raw.githubusercontent.com/elblogbruno/SpotDownloader/master/CredentialImage.png)

## How to use it.
Usage. Run python SpotDownloader.py -h to get information on how to use it.

usage: SpotDownloader.py [-h] [-v] [-u USERNAME] [-s SAVE_LOCATION] [-p URL]

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         Display more information on downloader.
  -u USERNAME, --username USERNAME
                        Spotify Username.
  -s SAVE_LOCATION, --save_location SAVE_LOCATION
                        Place where to save songs.
  -p URL, --url URL     Spotify playlist url to get the songs from.

## Credits
If you like this piece of software, I invite you to gently reach out to my personal website: elblogdebruno.com.
