import time
import pync


def notify(title, message):
    pync.notify(message, title=title, open='https://google.com/', sender='com.apple.launchpad.launcher')
    # sleep for call terminal-notifier
    # https://stackoverflow.com/questions/37010132/launchd-python-notifier-notify-not-producing-expected-output
    time.sleep(0.1)
