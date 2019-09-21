import os
import sys
import time
import twitter
from tqdm import tqdm
from datetime import datetime

from .db_utils import DB


__summary__ = 'SQL queries separated from code for readability'
__author__ = 'Ryan Callihan'
__version__ = '1.0.0'
__maintainer__ = 'Ryan Callihan'
__email__ = 'ryancallihan@gmail.com'


class TwitterScraper:

    """
    Easy to use stream scraper for twitter using python-twitter
    """
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
        self._log = open('./exception.log', 'w+', encoding='utf-8')

    def _start_stream(self, **kwargs):

        self._stream = self._api.GetStreamFilter(**kwargs)

    @staticmethod
    def _process_tweet(tweet):
        """
        Extracts the pertinent information from a tweet.

        :param tweet: Scraped tweet
        :type tweet: dict
        :return:
        """
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
            tweet.get('user', '').get('screen_name', ''),
            tweet.get('user', '').get('location', ''),
            tweet.get('user', '').get('description', ''),
            tweet.get('user', '').get('verified', ''),
            tweet.get('user', '').get('followers_count', ''),
            tweet.get('user', '').get('friends_count', ''),
            tweet.get('user', '').get('favourites_count', ''),
            tweet.get('user', '').get('statuses_count', ''),
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

    def _write_exception(self, e):
        self._log.write('{} - Exception: {}\n'.format(datetime.now().strftime("%m-%d-%Y:%H:%M:%S"), e))

    def scrape(self, **kwargs):
        """
        Performs actual scraping and handles exceptions

        :param kwargs: (optional) Arguments will replace args given at initialization
        :type kwargs: dict
        :return:
        """
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
                except OSError as e:
                    self._write_exception(e)
                    time.sleep(3)
                    self._start_stream(**self._kwargs)
                except Exception as e:
                    self._write_exception(e)
        except KeyboardInterrupt:
            self._db.close()
            print('\n\n{}\nClosing. Scraped {} tweets\n\n'
                  'Scraper run for {:.2f} minutes\n{}\n\n'.format(sep,
                                                                  self._scrape_cnt,
                                                                  (time.time() - self._start_time) / 60,
                                                                  sep))
            self._log.close()
            try:
                sys.exit(0)
            except SystemExit:
                os._exit(0)
