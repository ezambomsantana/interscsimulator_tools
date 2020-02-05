import xmltodict
import utm
import pyproj
import openrouteservice

csv_file = "../data/alts.csv"
mydict = []
with open(csv_file, mode='r') as infile:
    reader = csv.reader(infile, delimiter=";")
    mydict = {rows[0]:rows[1] for rows in reader}
    
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

            client = openrouteservice.Client(key='5b3ce3597851110001cf6248221d6f34d0204f47a619667c177f6459') # Specify your personal API key

            print(x1, y1)

            routes = client.elevation_point('point', (y1, x1))
            print(routes)
            alt = routes['geometry']['coordinates'][2]

            print(geometry)

            mydict[element['@id']] = alt

        except:
            print("An exception occurred")
            break

    
print(mydict)
