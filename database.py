import psycopg2
import config

try:
    if (config.dbusername and config.dbpassword):
        conn = psycopg2.connect("dbname='%s' host='%s' user='%s' password='%s'" % (config.dbname, config.host, config.dbusername, config.dbpassword))
    else:
        conn = psycopg2.connect("dbname='%s' host='%s'" % (config.dbname, config.host))
    cur = conn.cursor()
except:
    print "I am unable to connect to the database"

