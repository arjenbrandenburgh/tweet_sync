import tweepy
import config
import database
import screenshot
import os.path

# Twitter initialization
auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_secret)
auth.set_access_token(config.access_key, config.access_secret)
api = tweepy.API(auth)

tweets_seen = []

try:
    # Get the last 50 statusses
    statuses = api.user_timeline(screen_name = config.twitter_screenname, count = 50)
    for s in statuses:
        database.cur.execute("SELECT id FROM tweets WHERE tweet_id = %s;", [s.id])
        if database.cur.rowcount == 0:
            database.cur.execute("INSERT INTO tweets (tweet_id, text, screen_name, author_id, created_at, inserted_at) VALUES (%s, %s, %s, %s, %s, current_timestamp);", (s.id, s.text, s.author.screen_name, s.author.id, s.created_at))
            database.conn.commit()

        tweets_seen.append(s.id)

except tweepy.error.TweepError:
    print "Whoops, could not fetch tweets!"
except UnicodeEncodeError:
    pass
finally:
    database.cur.close()
    database.conn.close()

for tweet_id in tweets_seen:
    filename = "%s/%i.png" % (config.images_path, tweet_id)
    if not os.path.isfile(filename):
        url = "https://twitter.com/%s/status/%i" % (config.twitter_screenname, tweet_id)

        screenshot.get_screen_shot(
            url=url,
            filename=filename
        )

database.cur.close()
database.conn.close()