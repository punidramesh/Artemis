import requests, json
import psycopg2
import itertools

# Generate a list with the fields zipped together
def getJSON():
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

def contextPass():

    death = []
    confirmed = []
    recovered = []
    country = []

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
    for r in records:
        dict  = {}
        dict['cd'] = r['cd']
        dict['cn'] = r['cn']
        top.append(dict)
    top = top[0:5] 
    dict['countries'] = top  
    return dict 