#!/bin/sh

if [ `id -u` -ne 0 ]
then
  echo "Please run this script with root privileges!"
  echo "Try again with sudo."
  exit 0
fi

echo "This script will install SpotDownloader"
echo "SpotDownloader will install necessary dependencies for program to work"
echo "Do you wish to continue? (y/n)"

while true; do
  read -p "" yn
  case $yn in
      [Yy]* ) break;;
      [Nn]* ) exit 0;;
      * ) echo "Please answer with Yes or No [y|n].";;
  esac
done

echo ""
echo "============================================================"
echo ""
echo "Installing necessary dependencies... (This could take a while)"
echo ""
echo "============================================================"
apt-get update
apt-get install -y  python-pip git ffmpeg jq python3-pip python3.6
echo "============================================================"
if [ "$?" = "1" ]
then
  echo "An unexpected error occured during apt-get!"
  exit 0
fi



echo ""
echo "============================================================"
echo ""
echo "Configuring Spotify Credentials..."
echo ""
echo "============================================================"
echo "All this data asked here is needed to access your private playlist. To get started,  create an app on https://developers.spotify.com/, and get all the data that will be asked."
echo ""


echo "Tell me your spotify client ID: "
read clientId

echo "Tell me your spotify client SECRET ( It is very secret booo!): "
read clientSecret

echo "Tell me your spotify redirect URI: "
read redirectUri

jq -n   --arg id "$clientId"  --arg redirect "$redirectUri" \--arg secret "$clientSecret"  '{ "SPOTIPY_CLIENT_ID":"\($id)","SPOTIPY_CLIENT_SECRET":"\($secret)","SPOTIPY_REDIRECT_URI":"\($redirect)" }' > temp_keys.json 

mv temp_keys.json keys.json

echo "To set them manually (if you need to)"
echo "Open the keys.json file"

echo ""
echo "============================================================"
echo ""
echo "Cloning project from GitHub.."
echo ""
echo "============================================================"

if ! [ -x "$(command -v pip3)" ]; then
  echo 'Error: PIP software for python3 (pip3) is not installed. I will install it for you!' >&2
  curl "https://bootstrap.pypa.io/get-pip.py" -o "get-pip.py"
  python3 get-pip.py --user 
fi

pip3 install SpotDownloader

if [ "$?" = "1" ]
then
    echo "An unexpected error occured during pip install!"
    exit 0
fi

echo "============================================================"
echo "Setup was successful."
echo "You can run 'python SpotDownloader.py -h' to see how to start downloading playlists!"
echo "============================================================"

sleep 2


exit 0
