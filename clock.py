from apscheduler.schedulers.blocking import BlockingScheduler
import json,requests, psycopg2
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "covid.settings")
import django
django.setup()
from artemis.models import GlobalStats
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
    d = GlobalStats(date = date,dead = dead,
            confirmed = confirmed, recovered = recovered)
    d.save() 
    print("Inserting data:", " ",date," ",dead," ",confirmed," ",recovered)         
    print("Done")
sched.start()