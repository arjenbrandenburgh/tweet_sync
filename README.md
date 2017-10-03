# Tweet Sync

> Python script to save all tweets from a screenname in a Postgres database and screenshot the tweets, so you'll have a copy in case a tweet gets removed.

## Overview

Twitter provides functionality for a user to download it's own history, but this isn't an easy task and you cannot do that for an account that isn't yours. Tweet Sync has two main programs. One is to download a user's last 3200 tweets (```tweet_dumper.py```), and to screenshot those in batches of 200. The other one is to just look at a user last 50 tweets and saves the ones we are not already aware of (```tweets.py```).

The output of these scripts are saved in a Postgres database.

## Dependencies

* `python` (2.7)
  * `tweepy`
  * `selenium`
  * `psycopg2`
* `PhantomJS` (2.1.1)
* `ImageMagick` (6.9)
* `PostgreSQL` (9.6)

## Installation

```sh
pip2 install -r requirements.txt
```

Make sure you install PhantomJS and ImageMagick. For MacOS:
```sh
brew install phantomjs
brew install ImageMagick@6
```

Create a PostgreSQL database, and create a table ```tweets```:
```sql
CREATE TABLE tweets(
    id SERIAL PRIMARY KEY,
    tweet_id BIGINT NOT NULL,
    text VARCHAR NOT NULL,
    screen_name VARCHAR NOT NULL,
    author_id INTEGER,
    created_at VARCHAR NOT NULL,
    inserted_at TIMESTAMP NOT NULL
);
```

Edit the configuration in ```config.py```. You'll need a Twitter consumer key, consumer secret, access key and access secret. Also enter the Twitter screenname you wish to download, and enter your Postgres credentials.

## Usage

#### Tweet Dumper

Download the last 3200 tweets of the configured screenname, save them and create screenshots. This process may take quite a while, since it has to screenshot one tweet at a time. 

```sh
python2.7 tweet_dumper.py
``` 

#### Tweets

Look at the last 50 tweets of the configured screenname, and determine which we already know. Then it will proceed with makings screenshots of these tweets.

```sh
python2.7 tweets.py
```

The default setting is 50 tweets, but you can change that to your needs. For my purposes, this script automatically runs every minute, so my assumption is that someone isn't tweeting more than 50 tweets a minute.


## Contributing

Bug reports and pull requests are welcome on GitHub at https://github.com/cybey/tweet_sync.
Contributions are greatly appreciated. 

## Contributors

| [<img src="https://avatars.githubusercontent.com/u/7848606?v=3" width="100px;"/><br /><sub>Arjen Brandenburgh</sub>](https://github.com/cybey) |
| :---: |

## License

The plugin is available as open source under the terms of the [MIT License](http://opensource.org/licenses/MIT).
