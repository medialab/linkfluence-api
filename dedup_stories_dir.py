import os, sys, json

if __name__ == '__main__':
    if len(sys.argv) < 3:
        sys.exit('USAGE : '+sys.argv[0]+' [stories dir] [dest JSON file]')
    destfile = sys.argv[2]
    arbre = os.walk(sys.argv[1])
    dup = set()
    rslt = []
    for subrep in arbre:
        for filename in subrep[2]:
            if filename.endswith('.json') and 'stories' in filename and os.stat(subrep[0]+filename).st_size != 0:
                basename = filename.split('.')[0]
                with open(subrep[0]+filename, 'r') as f:
                    for doc in json.load(f)['hits']:
                        if doc['story'] not in dup:
                            dup.add(doc['story'])
                            rslt.append(doc)
    with open(destfile, 'w') as f:
        json.dump(rslt, f)