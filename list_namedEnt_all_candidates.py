import json, csv, sys, os
from os.path import join, isfile

if __name__ == '__main__':
    if len(sys.argv) < 3:
        sys.exit('USAGE : '+sys.argv[0]+' [dir path] [destCSV]')

    folder = sys.argv[1]
    dedup_set = set()
    with open(sys.argv[2], 'w') as g:
        dest_CSV = csv.writer(g)
        dest_CSV.writerow(['Weekly_Daily', 'NamedEntity'])

        for path in os.listdir(folder):
            full_path = join(folder, path)
            if not isfile(full_path) or \
               not path.endswith('.json') or \
               not path.startswith('namedEntities'):
                continue
            category = path.split('_')[2]
            with open(full_path, 'r') as f:
                doc_list = json.load(f)
                for doc in doc_list:
                    if 'namedEntitie' in doc and doc['namedEntitie'] is not None:
                        namedEnt = doc['namedEntitie']
                        if (category, namedEnt) not in dedup_set:
                            dest_CSV.writerow([category, namedEnt])
                            dedup_set.add((category, namedEnt))
