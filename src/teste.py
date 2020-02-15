import xmltodict
import utm
import pyproj
import openrouteservice
import csv
import pandas as pd

i = 0 
with open('../data/labeled_network.xml') as fd:
    doc = xmltodict.parse(fd.read())
    
    for element in doc['network']['nodes']['node']:
        i = i + 1

    
print(i)