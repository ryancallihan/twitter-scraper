import json
import argparse

from twitter_scraper.twitter_scraper import TwitterScraper


__summary__ = 'SQL queries separated from code for readability'
__author__ = 'Ryan Callihan'
__version__ = '1.0.0'
__maintainer__ = 'Ryan Callihan'
__email__ = 'ryancallihan@gmail.com'


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--keys', type=str, nargs=1, required=False, default=[None], help='(str) Path to json file with keys')
    parser.add_argument('--ckey', type=str, nargs=1, required=False, default=[None], help='(str) Consumer Key')
    parser.add_argument('--csec', type=str, nargs=1, required=False, default=[None], help='(str) Consumer Secret')
    parser.add_argument('--akey', type=str, nargs=1, required=False, default=[None], help='(str) Access Key')
    parser.add_argument('--asec', type=str, nargs=1, required=False, default=[None], help='(str) Access Secret')
    parser.add_argument('--db', type=str, nargs=1, required=True, help='(str) Path to Database')
    parser.add_argument('--geo', type=str, nargs='+', required=False, default=[None], help='(str) Location (e.g. London: -0.648677 51.249855 0.314508 51.742847)')
    parser.add_argument('--users', type=str, nargs='+', required=False, default=[None], help='(str) User IDs to stream')
    parser.add_argument('--terms', type=str, nargs='+', required=False, default=[None], help='(str) Terms to steam')
    parser.add_argument('--lang', type=str, nargs='+', required=False, default=[None], help='(str) Languages to stream')
    parser.add_argument('--rt', type=str, nargs=1, required=False, default=[None], help='(bool) If True Remove Retweets')

    args = parser.parse_args()

    keys = args.keys[0]
    ck = args.ckey[0]
    cs = args.csec[0]
    ak = args.akey[0]
    ass = args.asec[0]
    db = args.db[0]
    geo = args.geo
    users = args.users
    terms = args.terms
    lang = args.lang
    rt = args.rt[0]

    if (keys is None) and (ck is None) and (cs is None) and (ak is None) and (ass is None):
        raise Exception('Must give either JSON path with keys, or individual access keys')

    if (geo == [None]) and (users == [None]) and (terms == [None]):
        raise Exception('Must give either location, term(s), or user(s)')

    if keys is not None:
        with open(keys, 'r', encoding='utf-8') as file:
            k = json.load(file)
            file.close()
        ck, cs, ak, ass = k['consumer_key'], k['consumer_secret'], k['access_key'], k['access_secret']

    vars = dict()
    if geo != [None]:
        vars['locations'] = ['{},{}'.format(geo[0], geo[1]), '{},{}'.format(geo[2], geo[3])]
    if users != [None]:
        vars['follow'] = users
    if terms != [None]:
        vars['track'] = terms
    if lang != [None]:
        vars['langauges'] = lang
    if rt is not None:
        rt = True
    else:
        rt = False

    print('Vars used for stream:')
    for k, v in vars.items():
        print('\t- {}: {}'.format(k, v))

    scraper = TwitterScraper(ck, cs, ak, ass, db, rt, **vars)
    scraper.scrape()
