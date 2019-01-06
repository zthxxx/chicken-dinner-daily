## What's this

1. Access to Wi-Fi [**captive portal**](https://en.wikipedia.org/wiki/Captive_portal) while every time the WLAN status changes

![portal-success](./docs/portal-success.png)

2. Punch in as **scheduled** tasks (like crontab but plist in macOS)

![punch-success](./docs/punch-success.png)

## Install

1. `cd` to your projects directory

2. run this command below:

   ```bash
   curl -sSL https://github.com/zthxxx/chicken-dinner-daily/raw/master/install.sh | bash
   ```

   that will clone this repo into current path (`./chicken-dinner`), and link it to `~/Library/Scripts/chicken-dinner`,
   
   then will open the config file to edit,
   
   finally, launch plists



## Config

replace your custom config in [config/config.py](config/config.py)

```python
config = {
    'ssid_pattern': '', # regular expression to match which Wi-Fi SSID will trigger actions
    'login': {          # your user identity
        'username': '',
        'password': '', 
    },
    'punch': {
        'route': '',    # entry url for get CSRF token
        'api': '',      # API url to send punch post
    },
    'portal': {
        'route': '',    # entry url for get CSRF token
        'api': '',      # API url to send portal access post
    }
}
```



## Debug

### Check status

```bash
launchctl list | grep zthxxx
```

stdout will like this format

```bash
PID    Status  Label
-      0       com.zthxxx.ChickenDinnerDaily
-      0       com.zthxxx.AirportListener
```

exit code as `Status` 0 is OK, others are errors, to know any details of errors, see their logs



### Log

portal log file: `~/Library/Logs/AirportListener/on_network_change.log`

punch log file: `~/Library/Logs/ChickenDinnerDaily/punch.log`



### Restart

```bash
# restart portal service
launchctl stop com.zthxxx.AirportListener && launchctl start com.zthxxx.AirportListener

# restart punch service
launchctl stop com.zthxxx.ChickenDinnerDaily && launchctl start com.zthxxx.ChickenDinnerDaily

# check status
launchctl list | grep zthxxx
```

