import json
import csv
import sys

def toplinks_json2csv(f, g):
    jsonfile = json.load(f)
    csvfile = csv.writer(g)
    csvfile.writerow(['Date', 'URL', 'LRU', 'Document count'])
    for doc in jsonfile:
        csvfile.writerow([doc['date'], doc['url']['normalized'], doc['url']['reversed'], doc['counts']['doc']])

if __name__ == '__main__':
    if len(sys.argv) < 3:
        sys.exit('USAGE : '+sys.argv[0]+' [srcJSONfile] [destCSVfile]')
    with open(sys.argv[1], 'r') as f, open(sys.argv[2], 'w') as g:
        toplinks_json2csv(f, g)
