#!/usr/bin/env python

import os
import json
import time
import hashlib
import requests
from datetime import datetime, timedelta

from config import API_URL, PROJECT_ID, AUTH_TOKEN

for d in [".cache", "data"]:
    if not os.path.exists(d):
        os.makedirs(d)

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
    if res.status_code == 429:
        print "ERROR: while collecting", route, args
        print "too many calls for now, will retry in a few minutes"
        time.sleep(60)
        return download(route, args)
    data = res.json()
    with open(cache, "w") as f:
        json.dump(data, f)
    return data

# Get project settings
#settings = download()

# Get clusters
def collect_stories_period_page(frm, to, startIndex, rsltCount):
    return download("/stories", {
          "interval": "day",
          "from": frm,#"2016-05-01T00:00:00+01:00",
          "to": to,#"2017-07-01T00:00:00+02:00",
          "tz": "Europe/Paris",
          "limit": rsltCount,#2000,
          "start":startIndex,#i*2000
          "sortBy":"volumetry"
        })

def store_stories(startdate, enddate):
    sd = startdate.isoformat() + "+02:00"
    ed = enddate.isoformat() + "+02:00"
    for i in range(50):
        #i = j+31
        with open('stories-'+str(i*1000)+'-'+str((i+1)*1000-1)+'.json', 'w') as f:
    	    print i*1000
            json.dump(collect_stories_period_page(sd, ed, i*1000, 1000), f)
#print json.dumps(clusters)
# Get top keywords

def collect_words_period(frm, to, focus=None):
    args = {
      "fields": [],
      "metrics": ["doc", "reach", "impression"],
      "from": frm,
      "to": to,
      "tz": "Europe/Paris"
    }
    if focus:
        args["focuses"] = focus
    return download("/insights/cloud", args)["cloud"]

def collect_words(startdate, enddate, focus=None, days=1):
    results = {
      "namedEntities": [],
      "hashtags": [],
      "mentions": []
    }
    dat = startdate
    dt = dat.isoformat() + "+02:00"
    end = enddate
    while dat < end:
        print dat.isoformat()[:10]
        enddat = dat + timedelta(days=days)
        enddt = enddat.isoformat() + "+02:00"
        res = collect_words_period(dt, enddt, focus)
        for key in ["hashtags", "mentions", "namedEntities"]:
            k = key[:-1]
            for word, val in res[key].items():
                val["date"] = dat.isoformat()[:10]
                val[k] = word
                results[key].append(val)
        dat = enddat
        dt = dat.isoformat() + "+02:00"
    return results

format_for_csv = lambda x: unicode(x).encode("utf-8")
def store_words(startdate, enddate, days=1, focus=("", None)):
    words = collect_words(startdate, enddate, focus[1])
    suffix = ""
    if days == 1:
        suffix = "_daily"
    elif days == 7:
        suffix = "_weekly"
    if focus[1]:
        focus[0] = "_" + focus[0]
    for key in ["hashtags", "mentions", "namedEntities"]:
        headers = ["date", key[:-1], "doc", "impression", "reach"]
        with open(os.path.join("data", key + focus[0] + suffix + ".csv"), "w") as f:
            print >> f, ",".join(headers)
            for row in words[key]:
                print >> f, ",".join([format_for_csv(row[h]) for h in headers])
        with open(os.path.join("data", key + focus[0] + suffix + ".json"), "w") as f:
            json.dump(words[key], f)

if __name__ == "__main__":
    store_stories(datetime(2016, 5, 1), datetime(2017, 7, 1))
    for focus in [
      ("hamon", 83192),
      ("macron", 82709),
      ("fillon", 82719),
      ("melenchon", 82713),
      ("le-pen", 103736)
    ]:
        store_words(datetime(2017, 3, 1), datetime(2017, 7, 1), 1, focus)
        store_words(datetime(2016, 5, 1), datetime(2017, 7, 1), 7, focus)
