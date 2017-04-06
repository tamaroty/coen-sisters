# -*- coding: utf-8 -*-
import os
import sys
from datetime import datetime
from urllib2 import quote
from pytz import timezone
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator
from lxml import etree

IGNORED_ITEMS = [
    'MyStyles', 'RTLStylesheet', 'English', 'bg']
FEED_LINK = 'https://tamaroty.github.io/cohen-sisters/'
FEED_TITLE = u'האחיות כהן'
FEED_SUBTITLE = u"אתר ששרה'לה בטח היתה אוהבת"
FEED_LOGO = FEED_LINK+'pictures/logo.png'
FEED_LANGUAGE = 'he'
FEED_TZ = timezone('Asia/Jerusalem')

def is_item(i):
    return (
        i.has_attr('created') and
        i.has_attr('modified') and
        i.has_attr('title') and
        i['title'][0]!='$' and not
        i['title'] in IGNORED_ITEMS)

def parse_time(s):
    return FEED_TZ.localize(
        datetime.strptime(s[:14], '%Y%m%d%H%M%S'))

def main():
    here = os.path.dirname(sys.argv[0])
    if here:
        os.chdir(here)
    wiki = BeautifulSoup(open('../index.html'), 'html.parser')
    feed = FeedGenerator()
    feed.link(href=FEED_LINK, rel='alternate')
    feed.title(FEED_TITLE)
    feed.subtitle(FEED_SUBTITLE)
    feed.logo(FEED_LOGO)
    feed.language(FEED_LANGUAGE)
    items = sorted(
        wiki.find_all(is_item),
        key=lambda i: i['created'],
        reverse=True)
    feed.updated(parse_time(max([
        i['modified'] for i in items])))
    for i in items[:23]:
        entry = feed.add_entry()
        entry.link(
            href='{}#{}'.format(
                FEED_LINK,
                quote(i['title'].encode('utf-8'))))
        entry.title(i['title'])
        entry.published(parse_time(i['created']))
        entry.updated(parse_time(i['modified']))
    feed.rss_file('../rss.xml', pretty=True)
    print 'Feed is now up to date'

if __name__ == '__main__':
    main()
