import xmltodict
import utm

def calculate_distance(lat, lon):  
    return utm.to_latlon(lat, lon, 23, 'K')

with open('../data/map.xml') as fd:
    doc = xmltodict.parse(fd.read())
    
    for element in doc['network']['nodes']['node']:
        print(element['@id'])
        x = element['@x'].split(".")[0]
        y = element['@y'].split(".")[0]
        print(x)

        print(calculate_distance(x, y))