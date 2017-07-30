import os, json, re, urllib2, logging
from mastodon import Mastodon

INSTANCE_URL = 'https://tooot.im'
BOT_ID = 17058
APP_FOLDER = os.path.dirname(__file__)
CLIENT_ID_FILENAME = os.path.join(APP_FOLDER,'clientcred.txt')
ACCESS_TOKEN_FILENAME = os.path.join(APP_FOLDER,'usercred.txt')

JSON_FILENAME = os.path.abspath(
    os.path.join(APP_FOLDER,'../toots.json'))

SITE_URL = 'http://coensisters.org/'
RE_TIDDLE = re.compile('href="{}#([^"]*)"'.format(SITE_URL))

def get_tiddle(text):
    match = RE_TIDDLE.search(text) 
    if match:
        return unicode(
            urllib2.unquote(match.group(1).encode('ascii')), 'utf8')

def main():
    tootmap = {}
    try:
        tootmap = json.load(open(JSON_FILENAME))
    except IOError:
        pass
    
    m = Mastodon(
        client_id = CLIENT_ID_FILENAME,
        access_token = ACCESS_TOKEN_FILENAME,
        api_base_url = INSTANCE_URL)
    
    since_id = tootmap.get('since_id')
    print "since_id={}".format(since_id)
    if since_id:
        
        toots = m.account_statuses(BOT_ID, since_id=since_id)
    else:
        toots = m.account_statuses(BOT_ID)
    if not toots:
        return
    toots = m.fetch_remaining(toots)
    for toot in toots:
        t = get_tiddle(toot['content'])
        since_id = since_id and max(since_id, toot['id']) or toot['id']
        if t:
            tootmap[t] = toot['url']
            print u'{}: {}'.format(toot['id'], t)
    tootmap['since_id'] = since_id
    json.dump(tootmap, open(JSON_FILENAME,'w'), indent=4)

if __name__=='__main__':
    main()
