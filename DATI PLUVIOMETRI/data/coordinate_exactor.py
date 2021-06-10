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



query = "INSERT INTO dbo.COORD_PLUV (nome,territorio,lat,long) values(?,?,?,?)"


for k, file_name in enumerate(file_list):
    if not file_name.endswith(".xlsx"):
        print("bad file format {}".format(file_name))
        continue

    coordinate_sheet = pd.read_excel(file_name, sheet_name="Tabella delle stazioni")
    for i, row in coordinate_sheet.iterrows():
        nome = row["Nome della stazione"]
        provincia = row["Provincia"]
        lat = row["Latitudine (Gradi Centesimali)"]
        lon = row["Longitudine (Gradi Centesimali)"]

        
        if provincia == "FORLI-CESENA":
            provincia = "FORLICESENA"
        
        print("NOME: {}".format(nome))
        print("Provincia: {}".format(provincia))
        print("Latitudine: {}".format(lat))
        print("Longitudine: {}".format(lon))
        print("#######################################")
        cursor.execute(query, nome, provincia, lat, lon)
        cursor.commit()
print("bellali")
cursor.close()