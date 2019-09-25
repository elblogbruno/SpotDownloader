# SpotDownloader
![alt text](https://raw.githubusercontent.com/elblogbruno/SpotDownloader/master/SpotifyLogo.png)

This a sample and easy to use app in python that downloads all you music in .MP3 from a given spotify playlist!
Simply pass your username , playlist url , and get all your songs in high quality .MP3 or .aac or .webm or...!

## How to install
To install the program, fire up your linux distributed machine and run this command.

```
wget https://raw.githubusercontent.com/elblogbruno/SpotDownloader/master/setup.sh && sudo sh setup.sh
```
That's it.

The installation script will:
- Download SpotDownloader and install the necessary dependencies

## Configuration of the downloader. 
Change values inside SpotDownloader.py with your spotify account credentials. You can get your credentials from here:
https://developer.spotify.com/my-applications/#!/applications. You should click on create new client id, and fill up the form accordingly. 
For the redirect URI once you've created your client id, you can go to settings and set up your own. Maybe "https://www.google.com" can be a good one!
Edit the SpotDownloader.py file inside de SpotDownloader folder and fill up the values.

![alt text](https://raw.githubusercontent.com/elblogbruno/SpotDownloader/master/CredentialImage.png)

## How to use it.
Usage. Run python SpotDownloader.py -h to get more help information on how to use it.

usage: SpotDownloader.py [-h] [-v] [-u USERNAME] [-s SAVE_LOCATION] [-p URL] [-f FORMAT]

## Credits
If you like this piece of software, I invite you to gently reach out to my personal website: elblogdebruno.com.
##TODO
Android or web app.
Better login or setup process.
