import xmltodict
import utm
import pyproj
import openrouteservice

with open('../data/map.xml') as fd:
    doc = xmltodict.parse(fd.read())
    
    for element in doc['network']['nodes']['node']:
        print(element['@id'])
        x = element['@x'].split(".")[0]
        y = element['@y'].split(".")[0]

        x1, y1 = pyproj.transform('EPSG:32719', 'wgs84', x, y)

        client = openrouteservice.Client(key='5b3ce3597851110001cf6248221d6f34d0204f47a619667c177f6459') # Specify your personal API key

        print(x1, y1)

        routes = client.elevation_point('point', (y1, x1))
        print(routes)
        geometry = routes['geometry']['coordinates'][2]

        print(geometry)
        break
