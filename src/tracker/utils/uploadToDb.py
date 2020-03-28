import psycopg2
from tracker.utils.getData import getJSON

# Manipulating received data

livedata = list(getJSON())
death,confirmed,recovered,country = zip(*livedata)
size = len(death) - 1

# Queries
def upload():

    for i in range(size):
        try:
            # Open connection to database 
            conn = psycopg2.connect(
                    host = "localhost",
                    database="coronadb", 
                    user="postgres", 
                    password="G0odBy3C0rona")

            # Cursor
            cursor = conn.cursor()
            cursor.execute("INSERT INTO tracker_livedata (country, dead, confirmed, recovered) VALUES (%s,%s,%s,%s);",
            (death[i],confirmed[i],recovered[i],country[i]))
        except psycopg2.InterfaceError as exc:
            print (exc.message)
            conn = psycopg2.connect(
                        host = "localhost",
                        database="coronadb", 
                        user="postgres", 
                        password="G0odBy3C0rona")
            cursor = conn.cursor()    