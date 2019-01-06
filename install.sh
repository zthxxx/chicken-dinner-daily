#!/usr/bin/env bash

# curl -sSL https://github.com/zthxxx/chicken-dinner-daily/raw/master/install.sh | bash
# will clone this project to `./chicken-dinner` then link it to `~/Library/Scripts/chicken-dinner
# status show `launchctl list | grep zthxxx`

git clone --depth 1 https://github.com/zthxxx/chicken-dinner-daily.git chicken-dinner

mkdir -p ~/Library/Scripts
mkdir -p ~/Library/Logs/AirportListener ~/Library/Logs/ChickenDinnerDaily

ln -s "`pwd`/chicken-dinner" ~/Library/Scripts/

cd ~/Library/Scripts/chicken-dinner

perl -i -pe "s/Users\/zthxxx\/Library/Users\/${USER}\/Library/g" com.zthxxx.AirportListener.plist com.zthxxx.ChickenDinnerDaily.plist

ln -s "`pwd`/com.zthxxx.AirportListener.plist" ~/Library/LaunchAgents/
ln -s "`pwd`/com.zthxxx.ChickenDinnerDaily.plist" ~/Library/LaunchAgents/

cp config/config.py.template config/config.py

python3 -m venv venv && venv/bin/python -m pip install -r requirements.txt

vim config/config.py && (
    launchctl load ~/Library/LaunchAgents/com.zthxxx.AirportListener.plist
    launchctl load ~/Library/LaunchAgents/com.zthxxx.ChickenDinnerDaily.plist
)
