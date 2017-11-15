from toplinks_json2csv import toplinks_json2csv
import os, sys

if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit('USAGE : '+sys.argv[0]+' [toplinks dir]')
    arbre = os.walk(sys.argv[1])
    for subrep in arbre:
        for filename in subrep[2]:
            if filename.endswith('.json') and 'toplinks' in filename:
                basename = filename.split('.')[0]
                with open(subrep[0]+filename, 'r') as f, open(subrep[0]+basename+'.csv', 'w') as g:
                    toplinks_json2csv(f, g)