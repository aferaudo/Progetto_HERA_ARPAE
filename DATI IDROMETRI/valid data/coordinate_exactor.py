import pandas as pd
import os
import pyodbc

# DB connection for linux server machine
conn = pyodbc.connect('Driver={/opt/microsoft/msodbcsql17/lib64/libmsodbcsql-17.7.so.2.1};'
                      'Server=localhost;'
                      'Database=Hera;'
                      'UID=SA;'
                      'PWD=ServerVMHeraDB1*;')
cursor = conn.cursor()



file_list = os.listdir(".")



query = "INSERT INTO dbo.COORD_IDRO (nome,provincia,lat,long) values(?,?,?,?)"


for k, file_name in enumerate(file_list):
    if not file_name.endswith(".xlsx"):
        print("bad file format {}".format(file_name))
        continue

    coordinate_sheet = pd.read_excel(file_name, sheet_name="Tabella delle stazioni")
    if len(coordinate_sheet) > 1:
        temp = coordinate_sheet.head(1)
        nome = file_name.split("(")[0]
        provincia = temp["Provincia"].values[0]
        lat = temp["Latitudine (Gradi Centesimali)"].values[0]
        lon = temp["Longitudine (Gradi Centesimali)"].values[0]
    else:
        nome = coordinate_sheet["Nome della stazione"].values[0]
        provincia = coordinate_sheet["Provincia"].values[0]
        lat = coordinate_sheet["Latitudine (Gradi Centesimali)"].values[0]
        lon = coordinate_sheet["Longitudine (Gradi Centesimali)"].values[0]
    
    print("NOME: {}".format(nome))
    print("Provincia: {}".format(provincia))
    print("Latitudine: {}".format(lat))
    print("Longitudine: {}".format(lon))
    print("#######################################")
    cursor.execute(query, nome, provincia, lat, lon)
    cursor.commit()
print("bellali")
cursor.close()