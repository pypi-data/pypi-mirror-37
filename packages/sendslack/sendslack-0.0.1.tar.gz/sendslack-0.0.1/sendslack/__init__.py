import os
import requests


def msg(text, url=None):
    if url is None:
        try:
            url = os.environ['SLACK_URL']
        except:
            raise Exception('Pass url argument or Provide environment variable SLACK_URL')

    payload = {"text":  text,
        "icon_url": 'https://raw.githubusercontent.com/hongkunyoo/coffeewhale/master/coffee_whale_only_bg.png',
        "username": 'coffee-whale'}

    return requests.post(url, json=payload)
