import json

import requests


def get_top_podcasts(number=10):
  base_url = 'https://rss.itunes.apple.com/api/v1/us/podcasts/top-podcasts/all/{}/explicit.json'
  url = base_url.format(number)
  r = requests.get(url)
  if r.status_code == 200:
    results = json.loads(r.text)['feed']['results']
    return results
