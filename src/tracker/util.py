import requests, json, itertools

from .models import Livedata, GlobalStats
from math import log10,log 

# Generate a list with the fields zipped together
def getJSON():
    try:
        death = []
        confirmed = []
        recovered = []
        country = []
        url = "https://api.thevirustracker.com/free-api?countryTotals=ALL"
        data = requests.get(url).json()['countryitems'][0]
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

def upload():
    failsafe = False
    try:
        livedata = list(getJSON())
        confirmed,death,recovered,country = zip(*livedata)
        size = len(death) - 1
    except ValueError:   
        print ('Failed to get data') 
        failsafe = True

    if failsafe: return

    # Delete previous data
    Livedata.objects.all().delete()

    # Insert data into model
    for i in range(size):
        d = Livedata(country = country[i],dead = death[i],
            confirmed = confirmed[i], recovered = recovered[i])
        d.save()    

def topCountries():
    records = Livedata.objects.values() 
    top = []
    for r in records:
        if r['country'] != 'India' or r['country'] == 'China':
            top.append(r['country'])
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
                if int(i['confirmed']) >= 100:
                    confirmedlist.append(log(int(i['confirmed']),80))   
            finallist.append(confirmedlist)
    if parameter == 'confirmed':        
        return finallist
    elif parameter == 'country':
        return finaltop         


def getTimeline(parameter):
    data = GlobalStats.objects.values()
    dead = []
    date = []
    recovered = []
    confirmed = []
    for i in data:
        dead.append(i['dead'])
        date.append(i['date'][0:(len(i['date']) - 3)])
        recovered.append(i['recovered'])
        confirmed.append(i['confirmed'])
    if parameter == 'dead':
        return dead   
    elif parameter == 'confirmed':
        return confirmed 
    elif parameter == 'date':
        return date 
    elif parameter == 'recovered':
        return recovered          
   