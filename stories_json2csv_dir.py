from stories_json2csv import stories_json2csv
import os, sys

if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit('USAGE : '+sys.argv[0]+' [stories dir] [optional dest file]')
    arbre = os.walk(sys.argv[1])
    dup = set()
    for subrep in arbre:
        for filename in subrep[2]:
            if filename.endswith('.json') and 'stories' in filename and os.stat(subrep[0]+filename).st_size != 0:
                basename = filename.split('.')[0]
                destfile = subrep[0]+basename+'.csv' if len(sys.argv) == 2 else sys.argv[2] # Second arg is a merged csv file. If none, keep files separate.
                with open(subrep[0]+filename, 'r') as f, open(destfile, 'a') as g:
                    dup = stories_json2csv(f, g, write_header = dup == set(), dup_set = dup)