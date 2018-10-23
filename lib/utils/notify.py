import pync


def notify(title, message):
    pync.notify(message, title=title, open='https://google.com/', sender='com.apple.launchpad.launcher')
