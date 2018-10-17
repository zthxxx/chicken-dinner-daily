#!/usr/bin/env bash

# curl -sSL https://github.com/zthxxx/chicken-dinner-daily/raw/master/install.sh | bash

git clone --depth 1 https://github.com/zthxxx/chicken-dinner-daily.git ~/Downloads/chicken-dinner

ln -s ~/Downloads/chicken-dinner ~/Library/Scripts/

cd ~/Library/Scripts/chicken-dinner

sed "-i" "s/Users\/zthxxx\/Library/Users\/${USER}\/Library/g" com.zthxxx.AirportListener.plist

ln -s "`pwd`/com.zthxxx.AirportListener.plist" ~/Library/LaunchAgents/

cp config/config.py.template config/config.py

vim config/config.py


launchctl load ~/Library/LaunchAgents/com.zthxxx.AirportListener.plist
