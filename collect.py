#!/usr/bin/env python

import os, json
import hashlib
import requests

from config import API_URL, PROJECT_ID, AUTH_TOKEN

if not os.path.exists(".cache"):
    os.makedirs(".cache")

def download(route="", args={}):
    url = "%s%s%s.json" % (API_URL, PROJECT_ID, route)
    hashurl = hashlib.md5('%s/%s' % (url, json.dumps(args))).hexdigest()
    cache = os.path.join(".cache", hashurl)
    if os.path.exists(cache):
        with open(cache) as f:
            return json.load(f)
    headers = {
      "Authorization": "Bearer %s" % AUTH_TOKEN,
      "Content-Type": "application/json"
    }
    if not args:
        res = requests.get(url, headers=headers)
    else:
        res = requests.post(url, headers=headers, data=json.dumps(args))
    data = res.json()
    with open(cache, "w") as f:
        json.dump(data, f)
    return data

# Get project settings
#settings = download()

# Get clusters
for i in range(10):
#    i = j+8
    with open('stories-'+str(i*2000)+'-'+str((i+1)*2000-1)+'.json', 'w') as f:
    	print i*2000
        clusters = download("/stories", {
          "interval": "weeks",
          "from": "2016-05-01T00:00:00+01:00",
          "to": "2017-07-01T00:00:00+02:00",
          "tz": "Europe/Paris",
          "limit": 2000,
          "start":i*2000
        })
        json.dump(clusters, f)
#print json.dumps(clusters)
# Get top keywords
#keywords = download("/insights/cloud", {
#  "fields": [],
 # "metrics": ["doc", "reach", "impression"],
  #"from": "2016-05-01T00:00:00+01:00",
 # "to": "2017-07-01T00:00:00+02:00",
  #"tz": "Europe/Paris"
#})
