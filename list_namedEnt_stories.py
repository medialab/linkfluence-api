import json, sys, csv

if __name__ == '__main__':
    if len(sys.argv) < 3:
        sys.exit('USAGE : '+sys.argv[0]+' [srcJSON] [destCSV]')
    with open(sys.argv[1], 'r') as f, open(sys.argv[2], 'w') as g:
        doc_list = json.load(f)
        dest_CSV = csv.writer(g)
        dest_CSV.writerow(['Category', 'NamedEntity'])
        dedup_set = set()
        for doc in doc_list:
            if 'namedEntity' in doc['hit'] and doc['hit']['namedEntity'] is not None:
                for key, namedEntList in doc['hit']['namedEntity'].items():
                    for namedEnt in namedEntList:
                        if namedEnt not in dedup_set:
                            dest_CSV.writerow([key, namedEnt])
                            dedup_set.add(namedEnt)
