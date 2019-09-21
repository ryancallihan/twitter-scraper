# Twitter Scraper

An easy to use Twitter stream scraper.

#### _API Keys_

You can get API keys by creating an App on the [Twitter Developer](https://developer.twitter.com/) site

## Usage

### Example

```bash
python scrape.py --keys ./api_keys.json --db my_db.db --geo -0.648677 51.249855 0.314508 51.742847 --terms tube underground
```

### Arguments

#### API keys

You can either have your api keys stored in a `JSON` file

```
--keys [PATH_TO_FILE.json]
``` 

or enter them in via the command line.

```
--ckey [CONSUMER KEY]
--csec [CONSUMER SECRET]
--akey [ACCESS KEY]
--asec [ACCESS SECRET]
```

#### Database

Results will be stored in a database. If none exists, one will be created.

```
--db [PATH_TO_DB.db]
```

#### Scraping Options

_Geofence_

You can specify a geofence you want to scrape from by specifying the longitude and latitude of the SW and NE corners of the fence (in that order). London, for example, would be: `-0.648677 51.249855 0.314508 51.742847`.

These can easily be found in Google maps.

```
--geo [SW-LONG SW-LAT NE-LONG NE-LAT]
```

_Users_

You can specify which users to scrape from with their `user_id`

```
--users [USER_ID]
```

_Terms_

You can pass any specific terms you want to scrape

```
--terms [ALL_TERMS]
```

_Languages_

You can specify which langauges to scrape using the [ISO language code](https://www.loc.gov/standards/iso639-2/php/code_list.php)

```
--lang [LANGUAGES_TO_SCRAPE]
```

_Retweets_

If you would like to skip over retweets, simply pass any argument

```
--rt True
```

## Contributors

Ryan Callihan

## License

Licensed under the Apache License, Version 2.0 (the 'License');
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an 'AS IS' BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.