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

chaves = [
    '5b3ce3597851110001cf624887051db3a97b4cd28bfdb001dc78e025',
    '5b3ce3597851110001cf6248813eaabf7d4a4ea5bc6a33198e0002fa',
    '5b3ce3597851110001cf62489b0051e2356b4c01836db805ff886922',
    '5b3ce3597851110001cf62485349cbc08b96426bbe758858180a1503',
    '5b3ce3597851110001cf624810370a72249c4658ab1b22d88ab2ce4b',
    '5b3ce3597851110001cf6248e0cc6ae2dd724c33af067918f5324091',
    '5b3ce3597851110001cf62488777beff64334a6bae6f599728a0518f',
    '5b3ce3597851110001cf62489219515a87c94c19ad260bc8029f7831',
    '5b3ce3597851110001cf6248758acbaf705a464388f196e85dab1a24',
    '5b3ce3597851110001cf6248cb13af0221fc4a428ce063c17d56e592',
    '5b3ce3597851110001cf62481a64da65169f4dda99bfc69a6f841c65',
    '5b3ce3597851110001cf62487b0cd0cb920d45ffb8811f296b5044d5',
    '5b3ce3597851110001cf6248cdfd729c8d384fc4954873b2f2c2f26a',
    '5b3ce3597851110001cf6248cde1a5e95799410bb46073f792fcad73',
    '5b3ce3597851110001cf6248221d6f34d0204f47a619667c177f6459',
    '5b3ce3597851110001cf62485e1b4b1a6d2c4e90b22b0a6f1ff98e27',
    '5b3ce3597851110001cf62484bb60b7582ea443aa2e89bb73cb2c985',
    '5b3ce3597851110001cf62482e175cc938d542aabd8eaac5e217a5c0',
    '5b3ce3597851110001cf62483b85c67b106043d7a9c9921f6ec0a945',
    '5b3ce3597851110001cf6248396529ec9407473cb507315c7ab92eb7',
    '5b3ce3597851110001cf62480f68a481f69543088477def361e9517d',
]

key_number = 0
key = chaves[key_number]

with open('../data/labeled_network.xml') as fd:
    doc = xmltodict.parse(fd.read())
    
    for element in doc['network']['nodes']['node']:
        print(element['@id'])

        if element['@id'] in mydict:
            continue

        try:
            x = str(element['@x'])
            y = str(element['@y'])


            ##x1, y1 = pyproj.transform('EPSG:32719', 'wgs84', x, y)

            client = openrouteservice.Client(key=key) # Specify your personal API key
            print(y,x)

            routes = client.elevation_point('point', (float(x),float(y)))
            print(routes)
            alt = routes['geometry']['coordinates'][2]

            ids.append(element['@id'])
            alts.append(alt)
        except Exception as e:
            print('Failed to upload to ftp: '+ str(e))
            print("An exception occurred")
            if key_number > 17:
                break
            key_number = key_number + 1
            key = chaves[key_number]
            continue

    
frame = pd.DataFrame(list(zip(ids, alts)), columns =['id','alt'])
frame = frame.set_index('id')
print(frame)
teste = teste.append(frame)

print(teste)

teste.to_csv('../data/alts.csv')