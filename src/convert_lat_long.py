import xmltodict
import utm
import pyproj
import openrouteservice
import csv
import pandas as pd
   
ids = []
lats = []
longs = []

with open('../data/map.xml') as fd:
    doc = xmltodict.parse(fd.read())
    
    for element in doc['network']['nodes']['node']:
        print(element['@id'])

        x = str(element['@x'])
        y = str(element['@y'])


        x1, y1 = pyproj.transform('EPSG:32719', 'wgs84', x, y)

        ids.append(element['@id'])
        lats.append(x1)
        longs.append(y1)

    
frame = pd.DataFrame(list(zip(ids, lats, longs)), columns =['id','lat','lon'])
frame = frame.set_index('id')
frame.to_csv('../data/lat_long.csv')