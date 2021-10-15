import pandas as pd
import logging
from datetime import datetime

AI = ["TAG_TYPE", "INTERVAL", "START_TS", "TAG", "DESCRIZIONE TAG", "START_VALUE", "MINIMUM", "MAXIMUM", "MEAN", "LAST_VALUE"]
DI = ["TAG_TYPE", "INTERVAL", "START_TS", "TAG", "DESCRIZIONE TAG", "START_VALUE", "STATE_CHANGE", "TIME1", "LAST_VALUE"]


# Logging configuration
FORMAT = '%(levelname)s:%(asctime)-15s %(message)s'
logging.basicConfig(filename='automatism_hera.log', format=FORMAT, level=logging.DEBUG)

class ParserHera:

    _df_builder = {"data_ora": [], "livello": [], "portata": [], "cod_pozzo": [], "ambito": []}
    _df_builder_idro =  {"data_ora": [], "livello": [], "nome": []}

    def __init__(self, tags, file_level_list, file_portata_list):
        super().__init__()
        
        # Parameters:
        # - 1 pandas dataframe containing tags
        # - list of files containing level_data
        # - list of files containing portata_data
        self.tags = tags
        self.file_level_list = file_level_list
        self.file_portata_list = file_portata_list
    
    def _get_parameter_from_row(self, row, ai=True):
        # AI                            DI

        # TAG_TYPE;         0           TAG_TYPE;
        # INTERVAL;         1           INTERVAL;
        # START_TS;         2           START_TS; <--
        # TAG;              3           TAG;
        # DESCRIZIONE TAG;  4           DESCRIZIONETAG;
        # START_VALUE;      5           START_VALUE;
        # MINIMUM;          6           STATE_CHANGE;
        # MAXIMUM;          7           TIME1; <--
        # --> MEAN;         8           LAST_VALUE
        # LAST_VALUE        9

    
        data_ora = row[AI.index("START_TS")]
        tag = row[AI.index("TAG")]
        if ai:
            media = row[AI.index("MEAN")]
        else:
            media = row[DI.index("MEAN")]
        return tag, media, data_ora

    def _get_base_info_tags(self, tag_liv):
        cod_pozzo = self.tags[self.tags["TAG_LIV"]==tag_liv]["DENOMINAZIONE"].array[0]
        ambito = self.tags[self.tags["TAG_LIV"]==tag_liv]["TERRITORIO"].array[0]
        is_pozzo = self.tags[self.tags["TAG_LIV"]==tag_liv]["TYPE"].array[0]
        piano_campagna = self.tags[self.tags["TAG_LIV"]==tag_liv]["PIANO_CAMPAGNA"].array[0]

        return cod_pozzo, ambito, is_pozzo, piano_campagna

    def _process_portata(self, portata_tag, data_level, data_ora, infile=1):
        # Simple case, get the portata and then insert in in the db
        portata_empty = 0
        portata = -1
        if infile==1:
            for sensor_tag in portata_tag:
                # It is not possible to apply both filters at the same time
                value = data_level[data_level[AI.index("TAG")] == sensor_tag] # filtering by tag 
                value = value[value[AI.index("START_TS")] == data_ora] # filtering by time
                
                # keeping track of the portata index to delete
                # index_portata = value.index.values.astype(int)[0]

                # This is used to check if there exist a corresponding portata value.
                # If it does not exist the data will not be inserted
                if value.empty:
                    portata_empty += 1

                # here we can have multiple portata data, so we should sum it
                portata += value[AI.index("MEAN")].array[0]
            
            if portata_empty == len(portata_tag):
                portata = -1
        else:
            portata_tag = portata_tag[0] # For new sensor there exist only one tag
                
                # Least efficient solution: in this case we look in each file to find a valid row (valid row = right tag and data_ora)
            for file_name_portata in self.file_portata_list:
                portata_data = pd.read_csv("{}".format(file_name_portata), sep=";", header=None, index_col=False, parse_dates=[2])


                portata_data_filtered = portata_data[portata_data[DI.index("TAG")]==portata_tag] # filtering by tag 
                portata_data_filtered = portata_data_filtered[portata_data_filtered[DI.index("START_TS")]==data_ora] # filtering by time
                if portata_data_filtered.empty:
                    continue


                # Debug
                # print("portata of {}, {} found in {}, while source file is {}".format(code, data_ora, file_name_portata, file_name))
                portata = portata_data_filtered[DI.index("TIME1")].array[0]
                
                # Deleting data from csv
                # if delete_opt:
                #     portata_data = portata_data.drop(portata_data_filtered.index.values.astype(int)[0], axis=0)
                #     portata_data.to_csv("{}/{}".format(work_dir, file_name_portata), index=False, header=None,  sep=";")

        return round(portata, 3)

    def _get_real_level(self, piano_campagna, value, is_pozzo):
        if is_pozzo == 1:
            if piano_campagna > 0:
                real_level_value = round(value - piano_campagna,3)
            else:
                if value < 0:
                    real_level_value = round(value,3)
                else:
                    real_level_value = round(-value,3)
        else:
            real_level_value = piano_campagna + value
        
        return real_level_value

    def parse(self):
        """
        This method returns two pandas dfs containing the data
        to be inserted in the relational db.
        - first df: "DATA_ORA" "LIVELLO" "PORTATA" "COD_POZZO" "AMBITO"
        - second df (idro_level): "DATA_ORA" "LIVELLO" "NOME"
        """
        for file_name_level in self.file_level_list:
            if not file_name_level.endswith('.csv'):
                continue
            
            # Extracting dataframe
            data_level = pd.read_csv("{}".format(file_name_level), sep=";", header=None, index_col=False, parse_dates=[2])

            # Rows iterations
            for k, row in data_level.iterrows():
                tag, media, data_ora = self._get_parameter_from_row(row) # AI = True because here we analise only ai files
                
                # If TAG not in the list
                if len(self.tags[self.tags["TAG_LIV"]==tag]["DENOMINAZIONE"].array) == 0:
                    continue
                
                cod_pozzo, ambito, is_pozzo, piano_campagna = self._get_base_info_tags(tag_liv=tag)

                # This code could represent a "idrometro" or a "pozzo"
                if is_pozzo == 0:
                    # Case "idrometro" 
                    
                    real_idro_value = self._get_real_level(piano_campagna,media,is_pozzo)

                    logging.info("Idrometro: %s", "DATA_ORA: {}, NOME: {}, LIVELLO {}".format(data_ora, cod_pozzo, real_idro_value))
                    self._df_builder_idro["data_ora"].append(data_ora)
                    self._df_builder_idro["nome"].append(cod_pozzo)
                    self._df_builder_idro["livello"].append(real_idro_value)
                    continue
                

                # Is portata in file?
                is_portata_here = self.tags[self.tags["TAG_LIV"]==tag]["INFILE"].array[0]

                # Get portata tag
                portata_tag = self.tags[self.tags["TAG_LIV"]==tag]["TAG_PORTATA"].array

                portata = self._process_portata(portata_tag=portata_tag, data_level=data_level, data_ora=data_ora, infile=is_portata_here)
                
                real_value = self._get_real_level(piano_campagna, media, is_pozzo)
                logging.info("Pozzo: %s", "DATA ORA: {}, COD POZZO: {}, TAG: {}, MEDIA: {}, PIANO CAMPAGNA: {}, PORTATA: {}, REAL LEVEL VALUE: {}".format(data_ora, cod_pozzo, tag, media, piano_campagna, portata, real_value))

                if portata == -1:
                    logging.info("Not found a portata value, skip...")
                    continue
                
                self._df_builder["data_ora"].append(data_ora)
                self._df_builder["livello"].append(real_value)
                self._df_builder["portata"].append(portata)
                self._df_builder["cod_pozzo"].append(cod_pozzo)
                self._df_builder["ambito"].append(ambito)
        
        def_df_pozzi = pd.DataFrame(data=self._df_builder)
        def_df_idro = pd.DataFrame(data=self._df_builder_idro)
        return def_df_pozzi, def_df_idro

                
                    

