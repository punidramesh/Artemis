import psycopg2, requests
import datetime
from tracker.utils.getData import getJSON
failsafe = False
# Manipulating received data
try:
    livedata = list(getJSON())
    confirmed,death,recovered,country = zip(*livedata)
    size = len(death) - 1
except ValueError:   
    print ('Decoding JSON has failed') 
    failsafe = True
# Queries
def upload():
    if failsafe: return
    try:
        # Open connection to database 
        conn = psycopg2.connect(
                        host = "localhost",
                        port="5432",
                        database="coronadb", 
                        user="postgres", 
                        password="G0odBy3C0rona")

        conn.set_session(autocommit=True)
        # Cursor
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tracker_livedata")
        for i in range(size):
            cursor.execute("INSERT INTO tracker_livedata (country, dead, confirmed, recovered) VALUES (%s,%s,%s,%s);",
            (country[i],death[i],confirmed[i],recovered[i]))
    except psycopg2.InterfaceError as exc:
        print (exc.message)
        conn = psycopg2.connect(
                        host = "localhost",
                        database="coronadb", 
                        user="postgres", 
                        password="G0odBy3C0rona")
        cursor = conn.cursor()    