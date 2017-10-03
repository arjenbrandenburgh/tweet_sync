import tweepy
import config
import database
import screenshot
import os.path

# Twitter initialization
auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_secret)
auth.set_access_token(config.access_key, config.access_secret)
api = tweepy.API(auth)

try:
    statuses = api.user_timeline(screen_name = config.twitter_screenname, count = 200)
    while len(statuses) > 0:
        for s in statuses:
            # To remove duplicate entries
            # See http://initd.org/psycopg/docs/faq.html for "not all arguments converted during string formatting"
            database.cur.execute("SELECT id FROM tweets WHERE text = %s;", [s.text])
            if database.cur.rowcount == 0:
                database.cur.execute("INSERT INTO tweets (tweet_id, text, screen_name, author_id, created_at, inserted_at) VALUES (%s, %s, %s, %s, %s, current_timestamp);", (s.id, s.text, s.author.screen_name, s.author.id, s.created_at))
                database.conn.commit()

        oldest = statuses[-1].id - 1
        statuses = api.user_timeline(screen_name = config.twitter_screenname, count = 200, max_id = oldest)
        print "...%s tweets downloaded with %s as oldest" % (len(statuses), oldest)


except tweepy.error.TweepError:
    print "Whoops, could not fetch tweets!"
except UnicodeEncodeError:
    pass

database.cur.execute("SELECT tweet_id FROM tweets;")
for row in database.cur:
    filename = "%s/%i.png" % (config.images_path, row[0])
    if not os.path.isfile(filename):
        url = "https://twitter.com/%s/status/%i" % (config.twitter_screenname, row[0])

        screenshot.get_screen_shot(
            url=url,
            filename=filename
        )

database.cur.close()
database.conn.close()
