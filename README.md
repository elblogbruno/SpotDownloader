# SpotDownloader
![alt text](https://raw.githubusercontent.com/elblogbruno/SpotDownloader/master/Screenshots/SpotifyLogo.png)

This is a simple and easy to use app made in python that downloads all you music in .MP3 from a given spotify playlist, even your private ones!
Simply pass your username and get all your songs in high quality .MP3 or .aac or .webm or...!

## How to install
To install the program, fire up your linux distributed machine and run this command.

```
wget https://raw.githubusercontent.com/elblogbruno/SpotDownloader/master/setup.sh && sudo sh setup.sh
```
That's it.

The installation script will:
- Download SpotDownloader and install the necessary dependencies aswell as configure the Spotify needed keys.

## How to get your account specific credentials 
You can get your credentials from here:
https://developer.spotify.com/my-applications/#!/applications. 

## Step 1
You should click on create new client id, and fill up the form accordingly. 
![alt text](https://raw.githubusercontent.com/elblogbruno/SpotDownloader/master/Screenshots/createID.png)
![alt text](https://raw.githubusercontent.com/elblogbruno/SpotDownloader/master/Screenshots/FillUpForm.png)

## Step 2
For the redirect URI once you've created your client id, you can go to settings and set up your own. Maybe "https://www.google.com" can be a good one!
![alt text](https://raw.githubusercontent.com/elblogbruno/SpotDownloader/master/Screenshots/RedirectUri.png)

## Step 3
Give all this data when ask on the setup!

## Step 4
Have fun!

## How to use it.
Usage. Run SpotDownloader -h to get more help information on how to use it.

usage: SpotDownloader [-h] [-v] [-u USERNAME] [-s SAVE_LOCATION] [-f FORMAT]

## Credits
If you like this piece of software, I invite you to gently reach out to my personal website: brunomoya.com.

## TODO
Android or web app.
Better login or setup process.
