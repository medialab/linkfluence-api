#!/usr/bin/env python

import os, json
import hashlib
import requests
from datetime import datetime, timedelta

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
settings = download()

# Get clusters
clusters = download("/stories", {
  "interval": "weeks",
  "from": "2016-05-01T00:00:00+01:00",
  "to": "2017-07-01T00:00:00+02:00",
  "tz": "Europe/Paris"
})

# Get top keywords
def collect_words_period(frm, to):
    return download("/insights/cloud", {
      "fields": [],
      "interval": "weeks",
      "metrics": ["doc", "reach", "impression"],
      "from": frm,
      "to": to,
      "tz": "Europe/Paris"
    })["cloud"]

def collect_words_by_week():
    results = {
      "namedEntities": [],
      "hashtags": [],
      "mentions": []
    }
    dat = datetime(2016, 5, 1)
    dt = dat.isoformat() + "+02:00"
    while dt < "2017-07-01T00:00:00+02:00":
        print dt
        enddat = dat + timedelta(days=7)
        enddt = enddat.isoformat() + "+02:00"
        res = collect_words_period(dt, enddt)
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

if __name__ == "__main__":
    words = collect_words_by_week()
    for key in ["hashtags", "mentions", "namedEntities"]:
        with open(os.path.join("data", key + ".json"), "w") as f:
            json.dump(words[key], f)
        headers = ["date", key[:-1], "doc", "impression", "reach"]
        with open(os.path.join("data", key + ".csv"), "w") as f:
            print >> f, ",".join(headers)
            for row in words[key]:
                print >> f, ",".join([format_for_csv(row[h]) for h in headers])

