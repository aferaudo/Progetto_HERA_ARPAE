import pandas as pd
import logging
from datetime import datetime
import numpy as np
from informal_parser_interface import InformalParserInterface

AI_TAGS = ["TAG_TYPE", "INTERVAL", "START_TS", "TAG", "DESCRIZIONE TAG", "START_VALUE", "MINIMUM", "MAXIMUM", "MEAN", "LAST_VALUE"]
DI_TAGS = ["TAG_TYPE", "INTERVAL", "START_TS", "TAG", "DESCRIZIONE TAG", "START_VALUE", "STATE_CHANGE", "TIME1", "LAST_VALUE"]

def rotate(list_to_rotate, index):
    return list_to_rotate[index:] + list_to_rotate[:index]

class ParserHera(InformalParserInterface):

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
        
        # Read only once files containing level data
        logging.info("Loading portata files...")
        self.df_level_list = []
        self._initialize_level_dfs()
        logging.info("Done")

        # Read only once files containing digital portata data
        logging.info("Loading portata files...")
        self.df_portata_list = []
        self._initialize_portata_dfs()
        logging.info("Done")
    
    def _initialize_portata_dfs(self):
        """
        It initializes the list of pandas dataframes containing the digital portata data
        """
        for file_name_portata in self.file_portata_list:
            if not file_name_portata.endswith('.csv'):
                continue
            portata_data = pd.read_csv("{}".format(file_name_portata), sep=";", header=None, index_col=False, parse_dates=[2])
            self.df_portata_list.append(portata_data)
    
    def _initialize_level_dfs(self):
        """
        It initializes the list of pandas dataframes containing level data
        """
        for file_name_level in self.file_level_list:
            if not file_name_level.endswith('.csv'):
                continue
            level_data = pd.read_csv("{}".format(file_name_level), sep=";", header=None, index_col=False, parse_dates=[2])
            self.df_level_list.append(level_data)
        
    
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

    
        data_ora = row[AI_TAGS.index("START_TS")]
        tag = row[AI_TAGS.index("TAG")]
        if ai:
            media = row[AI_TAGS.index("MEAN")]
        else:
            media = row[DI_TAGS.index("MEAN")]
        return tag, media, data_ora

    def _get_base_info_tags(self, tag_liv):
        cod_pozzo = self.tags[self.tags["TAG_LIV"]==tag_liv]["DENOMINAZIONE"].array[0]
        ambito = self.tags[self.tags["TAG_LIV"]==tag_liv]["TERRITORIO"].array[0]
        is_pozzo = self.tags[self.tags["TAG_LIV"]==tag_liv]["TYPE"].array[0]
        piano_campagna = self.tags[self.tags["TAG_LIV"]==tag_liv]["PIANO_CAMPAGNA"].array[0]

        return cod_pozzo, ambito, is_pozzo, piano_campagna

    def _loop_file_search(self, dfs, data_ora, portata_tag, AI=True):
        # print("Do something!")
        for data in dfs:
            # print(data)
            portata = 0
            portata_empty = 0
            for sensor_tag in portata_tag:
                # Same index for AI and DI    
                value = data[data[AI_TAGS.index("TAG")]==sensor_tag] # filtering by tag 
                value = value[value[AI_TAGS.index("START_TS")]==data_ora] # filtering by time

                if value.empty:
                    portata_empty += 1
                    continue

                if AI:
                    # we can have multiple portata data, so we should sum it
                    portata += value[AI_TAGS.index("MEAN")].array[0]
                else:
                    portata += value[DI_TAGS.index("TIME1")].array[0]

            if portata_empty != len(portata_tag):
                # If I'm here it means that I found 
                # portata ready
                break
            else:
                # Portata not found
                portata = -1
            
        return portata
                 
    def _process_portata(self, portata_tag, data_level, data_ora, infile=1, source_file=None):
        """
        portata_tag: tag sensor
        data_level: dataframe containing level and portata_value values (useful when infile==1)
        data_ora: datetime of that rows
        infile: allows to understand where to serach the portata
        source_file: optional parameter used for logging purpose (typically it represents the name of the data_level file)
        Return portata
        """
        # Simple case, get the portata and then insert in in the db
        portata_empty = 0
        portata = 0
        if infile == 1:
            # AI file
            for sensor_tag in portata_tag:
                # It is not possible to apply both filters at the same time
                value = data_level[data_level[AI_TAGS.index("TAG")] == sensor_tag] # filtering by tag 
                value = value[value[AI_TAGS.index("START_TS")] == data_ora] # filtering by time

                # This is used to check if there exist a corresponding portata value.
                # If it does not exist the data will not be inserted
                if value.empty:
                    portata_empty += 1
                    continue

                # here we can have multiple portata data, so we should sum it
                portata += value[AI_TAGS.index("MEAN")].array[0]
            
            if portata_empty == len(portata_tag):
                portata = -1
                # check in other files
        else:
            # DI file
            portata_tag = portata_tag[0] # For new sensor there exist only one tag
                
            i = 0 # This index is used to get the file name (useful for logging procedure)
            
            portata = -1
            # More efficient solution: files are already loaded in memory. 
            # This allows to analyse directly the dataframe without reading each time the file
            for portata_data in self.df_portata_list:
                
                portata_data_filtered = portata_data[portata_data[DI_TAGS.index("TAG")]==portata_tag] # filtering by tag 
                portata_data_filtered = portata_data_filtered[portata_data_filtered[DI_TAGS.index("START_TS")]==data_ora] # filtering by time
                if portata_data_filtered.empty:
                    i += 1  
                    continue
                
                if not source_file is None:
                    # Used for debugging
                    date_level = datetime.strptime(source_file[4:18], "%Y%m%d%H%M%S")
                    date_portata = datetime.strptime(self.file_portata_list[i][4:18], "%Y%m%d%H%M%S")

                    if date_level.weekday() != date_portata.weekday():
                        logging.debug("%s", "Portata source file {}; Level source file {}; datetime row {}".format(self.file_portata_list[i], source_file, data_ora))
                i += 1 

                # portata ready
                portata = portata_data_filtered[DI_TAGS.index("TIME1")].array[0]
                
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
            real_level_value = round((piano_campagna + value), 3)
        
        return real_level_value

    def parse(self):
        """
        This method returns two pandas dataframes containing the data
        to be inserted in the relational db.
        - first df: "DATA_ORA" "LIVELLO" "PORTATA" "COD_POZZO" "AMBITO"
        - second df (idro_level): "DATA_ORA" "LIVELLO" "NOME"
        """
        counter = len(self.file_level_list)-1
        for index, data_level in enumerate(self.df_level_list):
            
            logging.info("Analysing %s", "file name: {} {} files left...".format(self.file_level_list[index], counter))
            counter -= 1

            # Initializing markers: markers[dim_df_level_data] = 0
            # Line processed marker = 1
            # Line not processed marker = 0
            if len(data_level.columns) <= 10:
                # No markers found
                markers = np.zeros(len(data_level), int) 
            else:
                # Load markers
                markers = data_level[10].array

            line_counter = 0

            # Rows iterations
            for k, row in data_level.iterrows():
                
                # If already analysed row skipping:
                if markers[k] == 1:
                    continue
                
                # print("Line to process: \n{}".format(row))
                tag, media, data_ora = self._get_parameter_from_row(row) # AI = True because here we analise only ai files
                
                # If TAG not in the list of level tags
                if len(self.tags[self.tags["TAG_LIV"]==tag]["DENOMINAZIONE"].array) == 0:
                    continue
                
                line_counter += 1 # debug
                cod_pozzo, ambito, is_pozzo, piano_campagna = self._get_base_info_tags(tag_liv=tag)

                # This code could represent a "idrometro" or a "pozzo"
                if is_pozzo == 0:
                    # Case "idrometro" 
                    real_idro_value = self._get_real_level(piano_campagna, media, is_pozzo)

                    logging.debug("Idrometro: %s", "DATA_ORA: {}, NOME: {}, LIVELLO {}".format(data_ora, cod_pozzo, real_idro_value))
                    self._df_builder_idro["data_ora"].append(data_ora)
                    self._df_builder_idro["nome"].append(cod_pozzo)
                    self._df_builder_idro["livello"].append(real_idro_value)
                    markers[k] = 1
                    continue
                

                # Is portata in file?
                is_portata_here = self.tags[self.tags["TAG_LIV"]==tag]["INFILE"].array[0]

                # Get portata tags
                portata_tags = self.tags[self.tags["TAG_LIV"]==tag]["TAG_PORTATA"]
                
                # Getting portata
                # portata = self._process_portata(portata_tag=portata_tags.array, data_level=data_level, data_ora=data_ora, infile=is_portata_here)
                if is_portata_here:
                    portata = self._loop_file_search(dfs=rotate(self.df_level_list, index), data_ora=data_ora, portata_tag=portata_tags.array)
                else:
                    portata = self._loop_file_search(dfs=self.df_portata_list, data_ora=data_ora, portata_tag=portata_tags.array, AI=False)

                real_value = self._get_real_level(piano_campagna, media, is_pozzo)
                logging.debug("Pozzo: %s", "DATA ORA: {}, COD POZZO: {}, TAG: {}, MEDIA: {}, PIANO CAMPAGNA: {}, PORTATA: {}, REAL LEVEL VALUE: {}, FILE LIVELLO: {}".format(data_ora, cod_pozzo, tag, media, piano_campagna, portata, real_value, self.file_level_list[index]))

                if portata == -1:
                    logging.debug("Not found a portata value for tag: {} data_ora: {} , skip...".format(tag, data_ora))
                    continue
                
                self._df_builder["data_ora"].append(data_ora)
                self._df_builder["livello"].append(real_value)
                self._df_builder["portata"].append(portata)
                self._df_builder["cod_pozzo"].append(cod_pozzo)
                self._df_builder["ambito"].append(ambito)

                # Line processed correctly: marked
                markers[k] = 1
                
            logging.debug("Processed Line %s", "in {}: {}".format(self.file_level_list[index], line_counter))
            data_level[10] = markers
            data_level.to_csv("{}".format(self.file_level_list[index]), date_format='%Y%m%d%H%M%S', index=False, header=None,  sep=";")            
        
        def_df_pozzi = pd.DataFrame(data=self._df_builder)
        def_df_idro = pd.DataFrame(data=self._df_builder_idro)
        

        return def_df_pozzi, def_df_idro

                
                    

