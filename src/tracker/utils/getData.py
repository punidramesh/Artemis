import requests, json

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
        #print(key," -> ",value[-1])  
        appendList(value[-1],death, confirmed, recovered, key, country)   

    # Sort lists based on highest no. of deaths    
    zipped = zip(death,confirmed,recovered,country)  

    return sorted(zipped, reverse = True)




