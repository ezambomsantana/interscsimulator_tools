# -*- coding: utf-8 -*-
import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
import csv
import unidecode
import math
import seaborn as sns
import geopy.distance
import utm
from shapely.geometry import shape, LineString, Polygon
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
import xmltodict
import pyproj
from scipy import spatial

top = Element('scmatrix')
top.set('version', '1.0')

print('1 - start reading the OD file')
data17 = pd.read_csv('../data/dados17.csv', dtype={'ZONA_O': str, 'ZONA_D': str}, header=0,delimiter=";", low_memory=False) 
data17 = data17.dropna(subset=['CO_O_X'])
data17['OX'] = data17['CO_O_X'].astype(int)
data17['OY'] = data17['CO_O_Y'].astype(int)
data17['DX'] = data17['CO_D_X'].astype(int)
data17['DY'] = data17['CO_D_Y'].astype(int)

def convert_lat_long(row, column_x, column_y):  
    return utm.to_latlon(row[column_x],row[column_y], 23, 'K')

data17['ORIGIN'] = data17.apply(lambda x: convert_lat_long(x,'CO_O_X', 'CO_O_Y'), axis=1)
data17['DESTINATION'] = data17.apply(lambda x: convert_lat_long(x,'CO_D_X', 'CO_D_Y'), axis=1)

modos17 = {0:'Other',1:'Work',2:'Work',3:'Work',4:'School',5:'Shopping',6:'Health',7:'Entertainment', 8:'House',9:'Seek Employment', 10: 'Personal Issues', 11:'Food'}
data17['MOTIVO_D'] = data17['MOTIVO_D'].replace(modos17)

modos17 = {0:'outros',1:'metro',2:'trem',3:'metro',4:'onibus',5:'onibus',6:'onibus',7:'fretado', 8:'escolar',9:'carro-dirigindo', 10: 'carro-passageiro', 11:'taxi', 12:'taxi-nao-convencional', 13:'moto', 14:'moto-passageiro', 15:'bike', 16:'pe', 17: 'outros'}
data17['MODOPRIN'] = data17['MODOPRIN'].replace(modos17)

data17 = data17[data17['MUNI_O'] == 36]
data17 = data17[data17['MUNI_D'] == 36]

print('1 - finish reading the OD file')

print('2 - start reading the map file')
ids = []
points = []
map = pd.read_csv('../data/lat_long.csv', header=0,delimiter=",", low_memory=False) 
for index, row in map.iterrows():
    id = row['id']
    x1 = row['lat']
    y1 = row['lon']
    ids.append(int(id))
    points.append((x1,y1))


print('2 - finish reading the map file')

tree = spatial.KDTree(points)

count_total = 0
count_reject = 0
print('2 - generating the trips')
for index, row in data17.iterrows():
    origin = row['ORIGIN']
    destination = row['DESTINATION']
    modo = row['MODOPRIN']
    hora = int(row['H_SAIDA'])
    minuto = int(row['MIN_SAIDA'])
    count = int(row['FE_VIA'])

    start = hora * 60 * 60 + minuto * 60

    if modo != 'bike':
        continue

    origin_point = tree.query(origin)
    dist_origin = origin_point[0]
    node_origin = origin_point[1]
    
    destination_point = tree.query(destination)
    dist_dest = destination_point[0]
    node_dest = destination_point[1]

    if dist_dest > 0.03 and dist_origin > 0.03:
        count_reject = count_reject + 1
        continue
    count_total = count_total + 1
    trip = SubElement(top, 'trip',
                             {
                              'name': 'trip' + str(count_total),  
                              'mode': modo,
                              'origin': str(ids[node_origin]),
                              'destination': str(ids[node_dest]),
                              'start': str(start),
                              'count': str(count),
                              })
print(count_reject)
print(count_total)
print(len(data17.index))

with open("trips.xml", "w") as f:
    f.write(tostring(top))