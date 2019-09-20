import os
import sys
import time
import twitter
from tqdm import tqdm
from db_utils import DB


class Scraper:

    def __init__(self, consumer_key, consumer_secret, access_key, access_secret, dbpath, rt, **kwargs):

        self._api = twitter.Api(consumer_key=consumer_key,
                                consumer_secret=consumer_secret,
                                access_token_key=access_key,
                                access_token_secret=access_secret,
                                cache=None,
                                tweet_mode='extended')
        self._rt = rt
        self._db = DB(dbpath)
        self._stream = None
        self._scrape_cnt = 0
        self._kwargs = kwargs
        self._start_time = time.time()

    def _start_stream(self, **kwargs):

        self._stream = self._api.GetStreamFilter(**kwargs)

    @staticmethod
    def _process_tweet(tweet):
        try:
            text = tweet.get('extended_tweet', {}).get('full_text', tweet['text']).replace('"', "'")
        except Exception:
            try:
                text = tweet['retweeted_status']['extended_tweet']['full_text'].replace('"', "'")
            except Exception:
                try:
                    text = tweet['text'].replace('"', "'")
                except Exception:
                    text = ''

        try:
            place = tweet.get('place', {}).get('full_name', '')
        except Exception:
            place = ''

        try:
            country_code = tweet.get['place'].get('country_code', '')
        except Exception:
            country_code = ''

        data = (
            tweet.get('created_at', ''),
            tweet.get('id_str', ''),
            text,
            tweet.get('user', {}).get('screen_name', ''),
            tweet.get('user', {}).get('location', ''),
            tweet.get('user', {}).get('description', ''),
            tweet.get('user', {}).get('verified', ''),
            tweet.get('user', {}).get('followers_count', ''),
            tweet.get('user', {}).get('friends_count', ''),
            tweet.get('user', {}).get('favourites_count', ''),
            tweet.get('user', {}).get('statuses_count', ''),
            place,
            country_code,
            tweet.get('retweeted', ''),
            tweet.get('lang', ''),
            tweet.get('timestamp_ms', '')
        )
        return data

    def _add_db(self, tweet):
        data = self._process_tweet(tweet)
        if not data[-3] and ('rt' not in self._kwargs):
            self._db.insert(data)
            self._scrape_cnt += 1
        else:
            pass

    def _set_kwargs(self, kwargs):
        self._kwargs = kwargs

    def scrape(self, **kwargs):
        sep = '-' * 30
        print('\n{}\nBeginning scrape.\nTo end, press "ctrl+c"\n{}\n\n'.format(sep, sep))
        self._start_time = time.time()
        if len(kwargs) > 0:
            self._set_kwargs(kwargs)
        self._start_stream(**self._kwargs)
        try:
            while True:
                try:
                    for tweet in tqdm(self._stream):
                        self._add_db(tweet)
                except Exception as e:
                    print('Exception:', e)
        except KeyboardInterrupt:
            self._db.close()
            print('\n\n{}\nClosing. Scraped {} tweets\n\n'
                  'Scraper run for {:.2f} minutes\n{}\n\n'.format(sep,
                                                                  self._scrape_cnt,
                                                                  (time.time() - self._start_time) / 60,
                                                                  sep))
            try:
                sys.exit(0)
            except SystemExit:
                os._exit(0)


if __name__ == '__main__':
    # consumer_key = 'rgHGRpTaCuQedIAIsAlZ8szki'
    # consumer_secret = 'OWzy5brRJr8SyYLCIWjByF7xgAF9FwxxkK8pbYRi7xWhNmXJLy'
    # access_token_key = '14754997-3RkZOXeoRbx9SKXTuEfF5MVDDTADGPFYZx5tMnI3X'
    # access_token_secret = 'gIXkvVkOkkFR91IalXYb5j4SA5J0RIFFFn3gjJkqj1bAC'
    # locations = ['-0.648677,51.249855', '0.314508,51.742847']
    # scraper = Scraper(consumer_key, consumer_secret, access_token_key, access_token_secret, 'D:/scraped_tweets/london_tweets.db',
    #                   locations=locations)
    # scraper.scrape()
    import json
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--keys', type=str, nargs=1, required=False, default=[None], help='(str) Path to json file with keys')
    parser.add_argument('--ckey', type=str, nargs=1, required=False, default=[None], help='(str) Consumer Key')
    parser.add_argument('--csec', type=str, nargs=1, required=False, default=[None], help='(str) Consumer Secret')
    parser.add_argument('--akey', type=str, nargs=1, required=False, default=[None], help='(str) Access Key')
    parser.add_argument('--asec', type=str, nargs=1, required=False, default=[None], help='(str) Access Secret')
    parser.add_argument('--db', type=str, nargs=1, required=True, help='(str) Path to Database')
    parser.add_argument('--geo', type=str, nargs='+', required=False, default=[None], help='(str) Location (e.g. London: -0.648677 51.249855 0.314508 51.742847  ')
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

    scraper = Scraper(ck, cs, ak, ass, db, rt, **vars)
    scraper.scrape()
