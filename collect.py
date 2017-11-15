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
    try:
        if not args:
            res = requests.get(url, headers=headers)
        else:
            res = requests.post(url, headers=headers, data=json.dumps(args))
    except requests.exceptions.ConnectionError:
        print "ERROR: while collecting", route, args
        print "no answer from server, will retry in a minute"
        time.sleep(60)
        return download(route, args)
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

# Get top links
def collect_top_links_period(frm, to, focus=None, rt=False):
    args = {
          "interval": "day",
          "from": frm,#"2016-05-01T00:00:00+01:00",
          "to": to,#"2017-07-01T00:00:00+02:00",
          "tz": "Europe/Paris",
          #"sortBy":"volumetry",
          "flag":{"rt":rt}
        }
    if focus:
        args["focuses"] = [{"id":focus,"include":True}]
        args["fctx"] = [focus]
    return download("/insights/most-shared-url", args)['mostSharedUrl']

def collect_top_links(startdate, enddate, focus=None, days=1, rt=False):
    results = []
    dat = startdate
    dt = dat.isoformat() + "+02:00"
    end = enddate
    while dat < end:
        print dat.isoformat()[:10], focus
        enddat = dat + timedelta(days=days)
        enddt = enddat.isoformat() + "+02:00"
        res = collect_top_links_period(dt, enddt, focus, rt)
        for val in res:
            val["date"] = dat.isoformat()[:10]
            results.append(val)
        dat = enddat
        dt = dat.isoformat() + "+02:00"
    return results

def store_top_links(startdate, enddate, days=1, focus=("", None), rt=False):
    top_links = collect_top_links(startdate, enddate, focus[1], days, rt)
    suffix = ""
    if focus[1]:
        suffix = "_" + focus[0]
    if days == 1:
        suffix += "_daily"
    elif days == 7:
        suffix += "_weekly"

#    headers = ["date", "normalized", "reversed"]
 #       with open(os.path.join("data", key + suffix + ".csv"), "w") as f:
  #          print >> f, ",".join(headers)
   #         for row in words[key]:
    #            print >> f, ",".join([format_for_csv(row[h]) for h in headers])
    with open(os.path.join("data", "toplinks" + suffix + ".json"), "w") as f:
         json.dump(top_links, f)
# Get clusters
def collect_stories_period_page(frm, to, startIndex, rsltCount, rt=False):
    return download("/stories", {
          "interval": "day",
          "from": frm,#"2016-05-01T00:00:00+01:00",
          "to": to,#"2017-07-01T00:00:00+02:00",
          "tz": "Europe/Paris",
          "limit": rsltCount,#2000,
          "start":startIndex,#i*2000
          "sortBy":"volumetry",
          "flag":{"rt":rt}
        })

def store_stories(startdate, enddate, rt=False):
    sd = startdate.isoformat() + "+02:00"
    ed = enddate.isoformat() + "+02:00"
    suffix = '' if rt == False else '-withRT'
    for i in range(100):
#        i = j+99
        rslt_size = 1000
        with open('stories-'+str(i*rslt_size)+'-'+str((i+1)*rslt_size-1)+suffix+'.json', 'w') as f:
    	    print i*rslt_size
            json.dump(collect_stories_period_page(sd, ed, i*rslt_size, rslt_size, rt), f)
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
        print dat.isoformat()[:10], focus
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
    words = collect_words(startdate, enddate, focus[1], days)
    suffix = ""
    if focus[1]:
        suffix = "_" + focus[0]
    if days == 1:
        suffix += "_daily"
    elif days == 7:
        suffix += "_weekly"
    for key in ["hashtags", "mentions", "namedEntities"]:
        headers = ["date", key[:-1], "doc", "impression", "reach"]
        with open(os.path.join("data", key + suffix + ".csv"), "w") as f:
            print >> f, ",".join(headers)
            for row in words[key]:
                print >> f, ",".join([format_for_csv(row[h]) for h in headers])
        with open(os.path.join("data", key + suffix + ".json"), "w") as f:
            json.dump(words[key], f)

if __name__ == "__main__":
    store_stories(datetime(2016, 5, 1), datetime(2017, 7, 1), False)
    for focus in [
      ("hamon", 83192),
      ("macron", 82709),
      ("fillon", 82719),
      ("melenchon", 82713),
      ("le-pen", 103736)
    ]:
        store_words(datetime(2017, 3, 3), datetime(2017, 7, 1), 1, focus)
        store_words(datetime(2016, 5, 1), datetime(2017, 7, 1), 7, focus)
        store_top_links(datetime(2017, 5, 1), datetime(2017, 7, 1), 1, focus)
