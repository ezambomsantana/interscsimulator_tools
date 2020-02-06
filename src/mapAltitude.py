import xmltodict
import utm
import pyproj
import openrouteservice
import csv
import pandas as pd


teste = pd.read_csv('../data/alts.csv', index_col='id')
print(teste)

csv_file = "../data/alts.csv"
mydict = []
with open(csv_file, mode='r') as infile:
    reader = csv.reader(infile, delimiter=",")
    mydict = {rows[0]:rows[1] for rows in reader}
    
ids = []
alts = []

with open('../data/map.xml') as fd:
    doc = xmltodict.parse(fd.read())
    
    for element in doc['network']['nodes']['node']:
        print(element['@id'])

        if element['@id'] in mydict:
            continue

        try:
            x = element['@x'].split(".")[0]
            y = element['@y'].split(".")[0]


            x1, y1 = pyproj.transform('EPSG:32719', 'wgs84', x, y)

            client = openrouteservice.Client(key='5b3ce3597851110001cf624810370a72249c4658ab1b22d88ab2ce4b') # Specify your personal API key

            print(x1, y1)

            routes = client.elevation_point('point', (y1, x1))
            print(routes)
            alt = routes['geometry']['coordinates'][2]

            ids.append(element['@id'])
            alts.append(alt)
        except:
            print("An exception occurred")
            break

    
frame = pd.DataFrame(list(zip(ids, alts)), columns =['id','alt'])
frame = frame.set_index('id')
print(frame)
teste = teste.append(frame)

print(teste)

teste.to_csv('../data/alts.csv')