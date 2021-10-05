import json
import math
import pyodbc

def computeAverageInCartesianCoord(list_lat, list_lon):

	sum_lat = 0
	sum_lon = 0
	for i in range(0, len(list_lat)):

		sum_lat = sum_lat + list_lat[i]
		sum_lon = sum_lon + list_lon[i]
	
	return sum_lat/len(list_lat), sum_lon/len(list_lat)
	

conn = pyodbc.connect('Driver={/opt/microsoft/msodbcsql17/lib64/libmsodbcsql-17.7.so.2.1};'
                      'Server=localhost;'
                      'Database=Hera;'
                      'UID=SA;'
                      'PWD=disiDatabase!;')
cursor = conn.cursor()

query = "INSERT INTO dbo.coord_pluv (cod_pluv,lat,long) values(?,?,?)"

with open("coord.json") as json_file:
	data = json.load(json_file)
	print(data)
	networks = dict()
	i = 0
	for p in data['result']['records']:
		network = p['network']
		lat = p['lat']/100000
		lon = p['lon']/100000
		id_pluv = "ID_{}".format(i)
		cursor.execute(query, id_pluv, lat, lon)
		i += 1
		
conn.commit()
print("bellali")
cursor.close()