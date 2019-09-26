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
apt-get install -y  python-pip git ffmpeg
echo "============================================================"
if [ "$?" = "1" ]
then
  echo "An unexpected error occured during apt-get!"
  exit 0
fi

pip install youtube-dl  spotipy pyfiglet

if [ "$?" = "1" ]
then
  echo "An unexpected error occured during pip install!"
  exit 0
fi

echo ""
echo "============================================================"
echo ""
echo "Cloning project from GitHub.."
echo ""
echo "============================================================"

sudo git clone https://github.com/elblogbruno/SpotDownloader.git

rm setup.sh
cd SpotDownloader/

echo "============================================================"
echo "Setup was successful."
echo "You can run 'python SpotDownloader.py -h' to see how to start downloading playlists!"
echo "============================================================"

sleep 2


exit 0
