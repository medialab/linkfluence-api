import os
import json
import time
import hashlib
import requests
from config import API_URL, PROJECT_ID, AUTH_TOKEN

def download(route="", args={}):
    url = "%s%s%s.json" % (API_URL, PROJECT_ID, route)
    hashurl = hashlib.md5(('%s/%s' % (url, json.dumps(args))).encode('utf-8')).hexdigest()
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
        print("ERROR: while collecting", route, args)
        print("no answer from server, will retry in a minute")
        time.sleep(60)
        return download(route, args)
    if res.status_code == 429:
        print("ERROR: while collecting", route, args)
        print("too many calls for now, will retry in a few minutes")
        time.sleep(60)
        return download(route, args)
    data = res.json()
    with open(cache, "w") as f:
        json.dump(data, f)
    return data
