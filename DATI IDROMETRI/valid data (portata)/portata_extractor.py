import pandas as pd
import os
import numpy as np
import pyodbc

column_name_0 = "Unnamed: 0"
column_name_1 = "Unnamed: 1"
column_name_2 = "Unnamed: 2"

file_list = os.listdir(".")
conn = pyodbc.connect('Driver={/opt/microsoft/msodbcsql17/lib64/libmsodbcsql-17.7.so.2.1};'
                      'Server=localhost;'
                      'Database=Hera;'
                      'UID=SA;'
                      'PWD=disiDatabase!;')
cursor = conn.cursor()

query = "INSERT INTO dbo.IDROMETRI (data_ora, Portata, nome) values(?,?,?)"


for k, file_name in enumerate(file_list):
    if not file_name.endswith(".xlsx"):
        print("bad file format {}".format(file_name))
        continue
    
    print("Analysing file {} {}/{}".format(file_name, k+1, len(file_list)))

    value_sheet = pd.read_excel(file_name, sheet_name="Tabella dei dati")
    name_sheet = pd.read_excel(file_name, sheet_name="Tabella delle stazioni")
    
    # There are stations with multiple sensors, so we'll have different names
    nomi = list()
    for i, row_name in name_sheet.iterrows():
        nomi.append(row_name["Nome della stazione"])

    value_sheet_formatted = value_sheet.drop(labels=[0,1,2,3,4,5], axis=0, inplace=False)

    i = 0
    found = False
    for index, row in value_sheet_formatted.iterrows():

        if (pd.isnull(row[column_name_0]) and pd.isnull(row[column_name_2])) or row[column_name_0] == "Inizio validità (UTC)":
            found = True
            continue
        
        if found:
            i = i+1
            found = False
            
        date = row["Unnamed: 0"]
        
        if pd.isnull(row["Unnamed: 2"]):
            
            portata = -99
        else:
            portata = float(row["Unnamed: 2"])

        # Write in DB
        cursor.execute(query, date, portata, nomi[i])
    cursor.commit()



cursor.close()