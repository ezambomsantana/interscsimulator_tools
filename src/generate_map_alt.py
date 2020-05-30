import utm
import pyproj
import openrouteservice
import csv
import pandas as pd
import xml.etree.ElementTree as ET
   
lats = {}
links = {}

alts = {}
map = pd.read_csv('../data/alts.csv', header=0,delimiter=",", low_memory=False) 
for index, row in map.iterrows():
    id = str(int(row['id']))
    alt = int(row['alt'])
    alts[id] = alt

xml_tree = ET.parse('../data/map.xml')
for elem in xml_tree.iter():
    if elem.tag == 'node':
        alt = alts[elem.attrib['id']]
        elem.attrib['z'] = str(alt)

    #lats[id] = (x, y)

new_xml_tree_string = ET.tostring(xml_tree.getroot())

with open('../data/map_with_z.xml', "wb") as f:
    f.write(new_xml_tree_string)