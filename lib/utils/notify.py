import pync


def notify(title, message):
    # wait for call terminal-notifier
    # https://stackoverflow.com/questions/37010132/launchd-python-notifier-notify-not-producing-expected-output/52968611#52968611
    pync.notify(message, title=title, open='https://google.com/', sender='com.apple.launchpad.launcher', wait=True)
