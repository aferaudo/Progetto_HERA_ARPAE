import pandas as pd
import os
import pyodbc
import math


sondedict = {
    "CAMP" : 17,
    "PIAN" : 15,
    "SECC" : 0,
    "A5" : 0,
    "A9" : 0,
    "A10" : 0,
    "B1" : 0,
    "MAN4" : 39.5,
    "MAN7" : 39.5,
    "MAG2" : 40
    }
querydict = {
    "BOLOGNA" : "INSERT INTO dbo.Bologna (data_ora,livello,portata,cod_pozzo) values(?,?,?,?)",
    "RIMINI" : "INSERT INTO dbo.Rimini (data_ora,livello,portata,cod_pozzo) values(?,?,?,?)",
    "MODENA" : "INSERT INTO dbo.Modena (data_ora,livello,portata,cod_pozzo) values(?,?,?,?)",
    "RAVENNA" : "INSERT INTO dbo.Ravenna (data_ora,livello,portata,cod_pozzo) values(?,?,?,?)",
    "FERRARA" : "INSERT INTO dbo.Ferrara (data_ora,livello,portata,cod_pozzo) values(?,?,?,?)",
    "FORLI'-CESENA" : "INSERT INTO dbo.ForliCesena (data_ora,livello,portata,cod_pozzo) values(?,?,?,?)",
    }

work_dir = os.getcwd()
file_list = os.listdir(work_dir)
conn = pyodbc.connect('Driver={/opt/microsoft/msodbcsql17/lib64/libmsodbcsql-17.7.so.2.1};'
                      'Server=localhost;'
                      'Database=Hera;'
                      'UID=SA;'
                      'PWD=disiDatabase!;')
cursor = conn.cursor()

for file in file_list:
    if not (file.endswith(".csv") or os.path.getsize(file) == 0):
        print("un file non e csv o è vuoto")
        continue
    city = file.split(".")[0]
    print("Analysing file {}/{}".format(work_dir, file))
    # Angelo Arpae
    # df = pd.read_csv("{}/{}".format(work_dir, file), parse_dates=['DATA_ORA'], dayfirst=True, sep=";")
    
    # Angelo Hera
    df = pd.read_csv("{}/{}".format(work_dir, file), parse_dates=['DATA_ORA'], dayfirst=True, sep=";")
    # df[df.COD_POZZO.eq("SECC")].to_csv("test.csv", index=False, sep=";")
    
    # Alberto
    # df = pd.read_csv("{}/{}".format(work_dir, file))
    print(df)
    
    # metti livello negativo

    for i, row in df.iterrows():
        # if df.at[i, "LIVELLO"] > 0:
        #     liv_sonda = sondedict[df.at[i, "COD_POZZO"]]
        #     df.at[i, "LIVELLO"] = df.at[i, "LIVELLO"] - liv_sonda
        data = df.at[i, "DATA_ORA"]
        livello = df.at[i, "LIVELLO"]
        portata = float(df.at[i, "PORTATA"])
        cod_pozzo = df.at[i, "COD_POZZO"]
        if not math.isnan(livello) and not math.isnan(portata):
            cursor.execute(querydict[city], data, livello, portata, cod_pozzo)
    conn.commit()     
    print("bellali")
 
cursor.close()    























