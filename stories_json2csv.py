#!/usr/bin/env python3
import json
import csv
import sys

def stories_json2csv(f, g):
    jsonfile = json.load(f)
    csvfile = csv.writer(g)
    csvfile.writerow([\
    'Story Id',\
    # Dates
    'First date',\
    'Threshold Date',\
    # Named Entities
    'Organization namedEntities',\
    'Person namedEntites',\
    'Location namedEntites',\
    'Miscellaneous namedEntites',\
    # Content info
    'Title',\
#    'Text',\
    'Language',\
    'Permalink',\
    # Document counts
    'Daily document count',\
    'Twitter document count',\
    'Website document count',\
    'Media document count',\
    'Blog document count',\
    'Facebook document count',\
    'Google+ document count',\
    'Positive tone document count',\
    'Neutral tone document count',\
    'Negative tone document count',\
    'Mixed tone document count',\
    'Total document count'\
    ])
    for doc in jsonfile['hits']:
        # Aggregation pre-process
        day_aggreg = []
        for i in doc['stats']['days']:
            day_aggreg.append(str(i['counts']['doc']))
        platform_aggreg = {}
        for i in doc['stats']['platforms']:
            platform_aggreg[i['term']] = str(i['counts']['doc'])
        tone_aggreg = {}
        for i in doc['stats']['tones']:
            tone_aggreg[i['term']] = str(i['counts']['doc'])
#        print('|'.join(day_aggreg))
#        print(json.dumps(doc, indent=4))
        # CSV
        platforms = [platform_aggreg.get(platform, '0') for platform in ['twitter', 'website', 'media', 'blog', 'facebook', 'gplus']]
        tones = [tone_aggreg.get(tone, '0') for tone in ['positive', 'neutral', 'negative', 'mixed']]
#        print(platforms is None, tones is None)
        line = [\
        doc['story'],\
        # Dates
        doc['stats']['days'][0]['date'],\
        doc['hit']['date'],\
        # Named Entities
        '|'.join(doc['hit']['namedEntity']['organization']) if 'namedEntity' in doc['hit'] and doc['hit']['namedEntity'] is not None else '',\
        '|'.join(doc['hit']['namedEntity']['person']) if 'namedEntity' in doc['hit'] and doc['hit']['namedEntity'] is not None else '',\
        '|'.join(doc['hit']['namedEntity']['location']) if 'namedEntity' in doc['hit'] and doc['hit']['namedEntity'] is not None else '',\
        '|'.join(doc['hit']['namedEntity']['misc']) if 'namedEntity' in doc['hit'] and doc['hit']['namedEntity'] is not None else '',\
        # Content info
        doc['hit'].get('title', ''),\
#        doc['hit']['text'],\
        doc['hit']['lang'],\
        doc['hit']['permalink'],\
        # Document counts
        '|'.join(day_aggreg)] + platforms + tones + [\
        doc['size']
        ]
        #csvfile.writerow([unicode(x).encode("utf-8") for x in line])
        csvfile.writerow(line)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        sys.exit('USAGE : '+sys.argv[0]+' [srcJSONfile] [destCSVfile]')
    with open(sys.argv[1], 'r') as f, open(sys.argv[2], 'w') as g:
        stories_json2csv(f, g)
