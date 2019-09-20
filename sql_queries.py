N_COLS = 16

CREATE_TABLE = '''CREATE TABLE tweets
                           (
                             created_at text, 
                             id text, 
                             text text, 
                             user text, 
                             user_location text,
                             bio text,
                             verified text,
                             followers integer,
                             following integer, 
                             favourites text,
                             n_tweets text,
                             tweet_location text,
                             country text,
                             retweet text,
                             lang text,
                             timestamp text
                           )'''

INSERT = 'INSERT INTO tweets VALUES ("{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}")'



