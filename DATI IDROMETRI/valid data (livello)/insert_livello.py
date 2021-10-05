import pyodbc
import os
import pandas as pd


file_list = os.listdir(".")


conn = pyodbc.connect('Driver={/opt/microsoft/msodbcsql17/lib64/libmsodbcsql-17.7.so.2.1};'
                      'Server=localhost;'
                      'Database=Hera;'
                      'UID=SA;'
                      'PWD=disiDatabase!;')
cursor = conn.cursor()

query = "INSERT INTO dbo.IDROMETRI_LIV (data_ora, livello, nome) values(?,?,?)"

for k, file_name in enumerate(file_list):
    if not file_name.endswith(".csv"):
        print("bad file format {}".format(file_name))
        continue
    
    print("Analysing file {} {}/{}".format(file_name, k+1, len(file_list)))
    idrometro = pd.read_csv(file_name, parse_dates=['DATA_ORA'], sep=";", decimal=",", dayfirst=True)
    print(idrometro)

    for i, row in idrometro.iterrows():
        #print(row)
        data_ora = idrometro.at[i,'DATA_ORA']
        livello = 8.8 + row['MEDIA']
        nome = 'FIUME PO' # Da cambiare
        # print("{}\t{}\t{}\t".format(nome,data_ora, livello))
        cursor.execute(query, data_ora, livello, nome)
        
    cursor.commit()
    print('bellali')

cursor.close()