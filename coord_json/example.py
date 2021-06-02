import json
import math
import pyodbc

def computeAverageInCartesianCoord(list_lat, list_lon):
	# for i in range(0, len(list_lat)):
	# 	# convert in degree coordinate
	# 	degree_lat = int(list_lat.get(i))
	# 	minutes_lat = (list_lat.get(i)-degree_lat) * 60
	# 	seconds_lat = int((minutes_lat.get(i)-int(minutes_lat)) * 60)
	# 	minutes_lat = int(minutes_lat)

	# 	degree_lon = int(list_lon.get(i))
	# 	minutes_lon = (list_lon.get(i)-degree_;pm) * 60
	# 	seconds_lon = int((minutes_lon.get(i)-int(minutes_lon)) * 60)
	# 	minutes_lon = int(minutes_lon)
	# sum_x = 0
	# sum_y = 0
	# sum_z = 0

	# for i in range(0, len(list_lat)):
	# 	lat_radians = list_lat[i] * math.pi / 180
	# 	lon_radians = list_lon[i] * math.pi / 180

	# 	sum_x = sum_x + math.sin(lat_radians) * math.cos(lon_radians)
	# 	sum_y = sum_y + math.sin(lat_radians) * math.sin(lon_radians)
	# 	sum_z = sum_z + math.cos(lat_radians)

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
                      'PWD=ServerVMHeraDB1*;')
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

		# key_lat = "{}_lat".format(network)
		# key_lon = "{}_lon".format(network)
		# if not key_lat in networks.keys():
		# 	networks[key_lat] = list()
		# 	networks[key_lon] = list()
		# networks[key_lat].append(lat/100000)
		# networks[key_lon].append(lon/100000)

	# result = dict()
	# for key in networks.keys():
	# 	if "_lon" in key:
	# 		continue
		
	# 	# x,y,z = computeAverageInCartesianCoord(networks.get(key), networks.get(key.replace("_lat", "_lon")))
	# 	# lat_rad = math.atan2(z, math.sqrt(x * x + y * y))
	# 	# long_rad = math.atan2(y, x)
	# 	# lat = lat_rad * 180 / math.pi
	# 	# lon = long_rad * 180 / math.pi
	# 	lat, lon = computeAverageInCartesianCoord(networks.get(key), networks.get(key.replace("_lat", "_lon")))
	# 	result[key.replace("_lat", "")] = (round(lat,5), round(lon,5))


	#  print(networks)
conn.commit()
print("bellali")
cursor.close()