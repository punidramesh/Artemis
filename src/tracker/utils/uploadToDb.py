import psycopg2, requests
import datetime
from tracker.utils.getData import getJSON

# Manipulating received data
x = datetime.datetime.now()
livedata = list(getJSON())
confirmed,death,recovered,country = zip(*livedata)
size = len(death) - 1
cur_confirmed = ''
cur_death = ''
cur_recovered = ''
cur_date = x.strftime("%x")
# Queries
def upload():

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
            if i == (size - 1):
                cur_death = death[i]
                cur_confirmed = confirmed[i]
                cur_recovered = recovered[i]
                cursor.execute("INSERT INTO tracker_globalstats (date,dead,confirmed,recovered) VALUES (%s,%s,%s,%s);",(cur_date, cur_death, cur_confirmed, cur_recovered))    
    except psycopg2.InterfaceError as exc:
        print (exc.message)
        conn = psycopg2.connect(
                        host = "localhost",
                        database="coronadb", 
                        user="postgres", 
                        password="G0odBy3C0rona")
        cursor = conn.cursor()    