import json, requests, sys, os

from APIdownload import download

def search_pub(query, frm="2016-05-01T00:00:00+02:00", to="2017-07-01T00:00:00+02:00", rsltLimit = 100):
    return download("/inbox/search", {
          "from": frm,#"2016-05-01T00:00:00+01:00",
          "to": to,#"2017-07-01T00:00:00+02:00",
          "tz": "Europe/Paris",
          "limit": rsltLimit,#2000,
#          "start":startIndex,#i*2000
          "sortBy":"radar.virality",
          "sortOrder":"desc",
          "query":query
#          "flag":{"rt":rt},
#          "metrics":["doc","impression","reach"]
        })

def make_search_query_from_url(base_url):
    prefixes = ['http://', 'https://', 'http://www.', 'https://www.']
    base_url = base_url.replace('https://', '').replace('http://', '').replace('www', '')
    return ' OR '.join(['"'+prefix+base_url+'"' for prefix in prefixes])

def make_search_query_from_url_list(url_list):
    return ' OR '.join([make_search_query_from_url(url) for url in url_list])

def make_wonderful_dict(decodex_dict):
    """Constitute a dict with the decodex id as key, and [[urls], entity_name, entity_trust_score, entity_description]."""
    algorithmically_constituted_dictionnary_with_python3_from_decodex_dictionnary = {}
    for url, decodex_id in decodex_dict['urls'].items():
        if decodex_id not in algorithmically_constituted_dictionnary_with_python3_from_decodex_dictionnary:
            algorithmically_constituted_dictionnary_with_python3_from_decodex_dictionnary[decodex_id] = [[url]]
        else:
            algorithmically_constituted_dictionnary_with_python3_from_decodex_dictionnary[decodex_id][0].append(url)
    for decodex_id in algorithmically_constituted_dictionnary_with_python3_from_decodex_dictionnary.keys():
        algorithmically_constituted_dictionnary_with_python3_from_decodex_dictionnary[decodex_id] += [decodex_dict['sites'][str(decodex_id)][i] for i in [2, 0, 1]]
    return algorithmically_constituted_dictionnary_with_python3_from_decodex_dictionnary

if __name__ == '__main__':
    if len(sys.argv) < 3:
        sys.exit('USAGE : '+sys.argv[0]+' [decodexJSON] [destDir]')
    wonderful_dict = make_wonderful_dict(json.load(open(sys.argv[1])))
    for decodex_id, decodex_info in wonderful_dict.items():
        filename = os.path.join(sys.argv[2], str(decodex_id)+'-'+decodex_info[1].replace(' ', '_').replace("'", "_").replace('://', '').replace('/', '_')+'.json')
        if not os.path.exists(filename):
            rslt = {'decodex_id':decodex_id, 'decodex_entity_name':decodex_info[1],\
            'decodex_entity_trust_score':decodex_info[2], 'decodex_entity_description':decodex_info[3]}
            query = make_search_query_from_url_list(decodex_info[0])
            print(decodex_info[1], end='...')
            rslt['radarly_hits'] = search_pub(query)['hits']
            if rslt['radarly_hits'] != []:
                with open(filename, 'w') as f:
                    json.dump(rslt, f)
                print('done')
            else:
                print('no match !')
        else:
            print('Skipping', decodex_info[1], ': already exists')
#    print(wonderful_dict)
    #print(make_search_query('sott.net'))
    