import requests, json
import psycopg2

# Append dictionary items into a list
def appendList(value,death, confirmed, recovered, key, country):
    death = death.append(int(value['deaths'])) 
    confirmed = confirmed.append(int(value['confirmed']))
    recovered = recovered.append(int(value['recovered']))
    country = country.append(key)

# Generate a list with the fields zipped together
def getJSON():
    death = []
    confirmed = []
    recovered = []
    country = []

    url = "https://pomber.github.io/covid19/timeseries.json"
    r = requests.get(url)

    with open('../src/timeseries.json',"w") as outfile:
        json.dump(r.json(), outfile)
    
    with open('../src/timeseries.json') as json_file: 
        data = json.load(json_file) 

    for key,value in sorted(data.items()): 
        appendList(value[-1],death, confirmed, recovered, key, country)   

    # Sort lists based on highest no. of deaths    
    zipped = zip(death,confirmed,recovered,country) 

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
    
    for i in record:
        dict = {}
        dict['cd'] = i[0]
        dict['d'] = i[1]
        dict['cn'] = i[2]
        dict['r'] = i[3]
        records.append(dict)
    return records