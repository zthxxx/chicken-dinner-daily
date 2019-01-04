#!/usr/bin/env bash

# curl -sSL https://gitcdn.xyz/repo/zthxxx/chicken-dinner-daily/master/install.sh | bash
# will download this project to `~/Downloads/chicken-dinner` and link to `~/Library/Scripts/chicken-dinner
# status show `launchctl list | grep zthxxx`

mkdir -p ~/Downloads ~/Library/Scripts

git clone --depth 1 https://github.com/zthxxx/chicken-dinner-daily.git ~/Downloads/chicken-dinner

ln -s ~/Downloads/chicken-dinner ~/Library/Scripts/

cd ~/Library/Scripts/chicken-dinner

sed "-i" "s/Users\/zthxxx\/Library/Users\/${USER}\/Library/g" com.zthxxx.AirportListener.plist com.zthxxx.ChickenDinnerDaily.plist

ln -s "`pwd`/com.zthxxx.AirportListener.plist" ~/Library/LaunchAgents/
ln -s "`pwd`/com.zthxxx.ChickenDinnerDaily.plist" ~/Library/LaunchAgents/

cp config/config.py.template config/config.py

python3 -m venv venv && venv/bin/python -m pip install -r requirements.txt

vim config/config.py && (
    launchctl load ~/Library/LaunchAgents/com.zthxxx.AirportListener.plist
    launchctl load ~/Library/LaunchAgents/com.zthxxx.ChickenDinnerDaily.plist
)
