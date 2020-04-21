from apscheduler.schedulers.blocking import BlockingScheduler
import json,requests, psycopg2
import datetime 
from pytz import utc
sched = BlockingScheduler()

@sched.scheduled_job('cron', day_of_week='mon-sun', hour=18, minute = 28,timezone=utc)
def scheduled_job():
    today = datetime.date.today()
    confirmed = []
    date = ""
    dead = []
    recovered = []
    url = "https://api.thevirustracker.com/free-api?global=stats"
    data = requests.get(url).json()
    data = data['results'][0]
    dead = data['total_deaths']
    recovered = data['total_recovered']
    confirmed = data['total_cases']
    date = str(today.month) + "/" +  str(today.day) + "/" + str(today.year%100)
    conn = psycopg2.connect(
                    host = "ec2-34-204-22-76.compute-1.amazonaws.com",
                    port="5432",
                    database="d9vtoshi8dsn03", 
                    user="vdzlfvisgqhtzp", 
                    password="0bcb8932ca66aa9650be5de340e40953cd6cb535af8a55b3b1e32b88f2ba807c")

    conn.set_session(autocommit=True)
    # Cursor
    cursor = conn.cursor()
    print("Inserting data:", " ",date," ",dead," ",confirmed," ",recovered)        
    cursor.execute("INSERT INTO artemis_globalstats (date,dead,confirmed,recovered) VALUES (%s,%s,%s,%s)",
                    (date,dead,confirmed,recovered))    
    print("Done")
sched.start()