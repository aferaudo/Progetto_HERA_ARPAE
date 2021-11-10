import logging
import pyodbc


querydict = {
    "BOLOGNA" : "INSERT INTO dbo.Bologna (data_ora,livello,portata,cod_pozzo) values(?,?,?,?)",
    "RIMINI" : "INSERT INTO dbo.Rimini (data_ora,livello,portata,cod_pozzo) values(?,?,?,?)",
    "MODENA" : "INSERT INTO dbo.Modena (data_ora,livello,portata,cod_pozzo) values(?,?,?,?)",
    "RAVENNA" : "INSERT INTO dbo.Ravenna (data_ora,livello,portata,cod_pozzo) values(?,?,?,?)",
    "FERRARA" : "INSERT INTO dbo.Ferrara (data_ora,livello,portata,cod_pozzo) values(?,?,?,?)",
    "FORLI'-CESENA" : "INSERT INTO dbo.ForliCesena (data_ora,livello,portata,cod_pozzo) values(?,?,?,?)",
    "IDROMETRO_LIV": "INSERT INTO dbo.IDROMETRI_LIV (data_ora, livello, nome) values(?,?,?)",
    # TODO add queries for PLUVIOMETRI and IDROMETRI
}

class DbManager:
    def __init__(self):
        super().__init__()
        # TODO implement dynamic configuration
        self.conn = pyodbc.connect('Driver={/opt/microsoft/msodbcsql17/lib64/libmsodbcsql-17.7.so.2.1};'
                      'Server=localhost;'
                      'Database=Hera;'
                      'UID=SA;'
                      'PWD=disiDatabase!;')
        self.cursor = self.conn.cursor()

    def __del__(self):
        self.cursor.close()

    def insert_pozzi(self, dataframe_pozzi):
        """Insert data into mssql db
        dataframe_pozzi: pandas dataframe containing pozzi data
        dataframe structure [data_ora, livello, portata, cod_pozzo, ambito]
        """
        for _, row in dataframe_pozzi.iterrows():
            data = row["data_ora"]
            livello = float(row["livello"])
            portata = float(row["portata"])
            cod_pozzo = row["cod_pozzo"]
            ambito = row["ambito"]
            self.cursor.execute(querydict[ambito], data, livello, portata, cod_pozzo)
        self.conn.commit()

    def insert_idro_level(self, dataframe_idro):
        """Insert Hera data into mssql db
        dataframe_idro: pandas dataframe containing idro data
        dataframe structure ["data_ora", "livello", "nome"]
        """
        for _, row in dataframe_idro.iterrows():
            data = row["data_ora"]
            livello = float(row["livello"])
            nome = row["nome"]
            self.cursor.execute(querydict["IDROMETRO_LIV"], data, livello, nome)
        self.conn.commit()

    # TODO 
    def insert_pluv(self, dataframe_pluv):
        print("Do something")

    def insert_idro_por(self, dataframe_idro):
        print("Do something")
    
