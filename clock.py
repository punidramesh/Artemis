from apscheduler.schedulers.blocking import BlockingScheduler
import json,requests, psycopg2
import datetime 
sched = BlockingScheduler()

@sched.scheduled_job('cron', day_of_week='mon-sun', hour=23, minute = 58)
def scheduled_job():
    today = datetime.date.today()
    confirmed = []
    date = []
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
                    host = "{}",
                    port="{}",
                    database="{}", 
                    user="{}", 
                    password="{}")

    conn.set_session(autocommit=True)
    # Cursor
    cursor = conn.cursor()
    cursor.execute("INSERT INTO artemis_globalstats (date,dead,confirmed,recovered) VALUES (%s,%s,%s,%s)",
                    date,dead,confirmed,recovered)
    conn.close()                

sched.start()