import requests, json
import psycopg2
import itertools
from math import log

# Generate a list with the fields zipped together
def getJSON():
    try:
        death = []
        confirmed = []
        recovered = []
        country = []

        url = "https://api.thevirustracker.com/free-api?countryTotals=ALL"
        r = requests.get(url)
        with open('timeseries.json',"w") as outfile:
            json.dump(r.json(), outfile)
        with open('timeseries.json') as json_file: 
            data = json.load(json_file)  
        data = data['countryitems'][0] 
        data = dict(itertools.islice(data.items(), (len(data) - 1)))   
        for value in data.values():
            death.append(value['total_deaths'])  
            confirmed.append(value['total_cases'])
            recovered.append(value['total_recovered'])
            country.append(value['title'])
        zipped = zip(confirmed,death,recovered,country) 
        return sorted(zipped, reverse = True)
    except ValueError:  # includes simplejson.decoder.JSONDecodeError
        print ('Decoding JSON has failed') 
        raise ValueError 

def connect():
    # Open connection to database
    conn = psycopg2.connect(
                        host = "localhost",
                        port="5432",
                        database="coronadb", 
                        user="postgres", 
                        password="G0odBy3C0rona")


    conn.set_session(autocommit=True)
    
    # Cursor
    return conn.cursor()

def contextPass():

    death = []
    confirmed = []
    recovered = []
    country = []

    # Cursor
    cursor = connect()

    # Execute queries
    cursor.execute("SELECT country,dead,confirmed,recovered FROM tracker_livedata")
    record = cursor.fetchall()
    records = []
    top = []
    for i in record:
        dict = {}
        dict['cd'] = i[0]
        dict['d'] = i[1]
        dict['cn'] = i[2]
        dict['r'] = i[3]
        records.append(dict)
    for r in records:
        top.append(r['cd'])
        top = top[0:4]    
    return records

def topCountries():
    records = contextPass()
    top = []
    dict = {}
    for r in records:
        top.append(r['cd'])
    top = top[0:5] 
    top.append('China')
    top.append('India')  
    return top

def getTopCountryHistory(parameter):
    url = "https://pomber.github.io/covid19/timeseries.json"
    r = requests.get(url).json()
    top = topCountries()
    finallist = [] 
    finaltop = []
    for key,value in sorted(r.items()): 
        confirmedlist = []
        if key in top or key == "US":
            finaltop.append(key)
            for i in value:
                if int(i['confirmed']) >= 50:
                    confirmedlist.append(log(int(i['confirmed'])))  
            finallist.append(confirmedlist)
    if parameter == 'confirmed':        
        return finallist
    elif parameter == 'country':
        return finaltop         


def getTimeline(parameter):
    cursor = connect()
    cursor.execute("SELECT dead FROM tracker_globalstats")
    dead = cursor.fetchall()
    cursor.execute("SELECT date FROM tracker_globalstats")
    date = cursor.fetchall()
    cursor.execute("SELECT confirmed FROM tracker_globalstats")
    confirmed = cursor.fetchall()   
    cursor.execute("SELECT recovered FROM tracker_globalstats")
    recovered = cursor.fetchall()      
    for i in range(len(dead)):
        dead[i] = int(dead[i][0])
        confirmed[i] = int(confirmed[i][0])
        recovered[i] = int(recovered[i][0])
        date[i] = str(date[i][0])
    if parameter == 'dead':
        return dead   
    elif parameter == 'confirmed':
        return confirmed 
    elif parameter == 'date':
        return date 
    elif parameter == 'recovered':
        return recovered          
   