import os
import pandas as pd
from datetime import datetime, timedelta
import logging
import argparse



queries = {
    "IDRO_LIV": "INSERT INTO dbo.IDROMETRI_LIV (data_ora, livello, nome)(?,?,?)", 
    "BOLOGNA": "INSERT INTO dbo.BOLOGNA (data_ora,livello,portata,cod_pozzo) values(?,?,?,?)",
    "MODENA": "INSERT INTO dbo.MODENA (data_ora,livello,portata,cod_pozzo) values(?,?,?,?)",
    "FORLICESENA": "INSERT INTO dbo.FORLICESENA (data_ora,livello,portata,cod_pozzo) values(?,?,?,?)",
    "RIMINI": "INSERT INTO dbo.RIMINI (data_ora,livello,portata,cod_pozzo) values(?,?,?,?)",
    "RAVENNA": "INSERT INTO dbo.RAVENNA (data_ora,livello,portata,cod_pozzo) values(?,?,?,?)",
    "FERRARA": "INSERT INTO dbo.FERRARA (data_ora,livello,portata,cod_pozzo) values(?,?,?,?)"
}



AI = ["TAG_TYPE", "INTERVAL", "START_TS", "TAG", "DESCRIZIONE TAG", "START_VALUE", "MINIMUM", "MAXIMUM", "MEAN", "LAST_VALUE"]
DI = ["TAG_TYPE", "INTERVAL", "START_TS", "TAG", "DESCRIZIONE TAG", "START_VALUE", "STATE_CHANGE", "TIME1", "LAST_VALUE"]


def get_parameter_from_row(row, ai=True):
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

def get_base_info_tags(tags, tag_liv):
    cod_pozzo = tags[tags["TAG_LIV"]==tag_liv]["DENOMINAZIONE"].array[0]
    ambito = tags[tags["TAG_LIV"]==tag_liv]["TERRITORIO"].array[0]
    is_pozzo = tags[tags["TAG_LIV"]==tag_liv]["TYPE"].array[0]

    return cod_pozzo, ambito, is_pozzo

    



# This script should read the data in RWAIyyyymmddhhmmss.csv RWDIyyyymmddhhmmss.csv and insert it into a database.
# Next it has to call the script that computes the status (monitor/status_monitor.py)
# Once a file has been analysed, it will be maintaned for 5 days as backup

FORMAT = '%(levelname)s:%(asctime)-15s %(message)s'


# Logging configuration
logging.basicConfig(filename='automatism_hera.log', format=FORMAT, level=logging.DEBUG)

# formatting data_parser
d = lambda x : datetime.strptime(x, "%Y%m%d%H%M%S")

dictionary = {"data_ora": [], "livello": [], "portata": [], "cod_pozzo": [], "ambito": []}

def main(argv):

    work_dir = argv.path
    delete_opt = argv.delete

    file_list = os.listdir(work_dir)
    tags = pd.read_excel('pozzi_tags/Tag Pozzi con Sonde_per TLC_1.xlsx') # File useful for tag match
    subset_file_list_portata = [name for name in file_list if "DI" in name]
    subset_file_list_level = [name for name in file_list if "AI" in name]
    now = datetime.now() # This is used to understand which file should be deleted

    for file_name in file_list:
        if not file_name.endswith('.csv'):
            continue
    
        # Filtering file name to get the datetime: used to determine file age
        date_level = datetime.strptime(file_name[4:18], "%Y%m%d%H%M%S")
        
        index_list = list()
        
        # These files will be read only for some kind of sensors
        if "DI" in file_name:
            print("File {} found, skipping...".format(file_name))
            continue

        # TODO Only today's files should be analysed
        # if day_difference.days == 0:
        #     print("Ok")

        data = pd.read_csv("{}/{}".format(work_dir, file_name), sep=";", header=None, index_col=False, parse_dates=[2])
        print(data)
        # Efficient implementation
        # portata_data = pd.read_csv("{}/RWDI{}.csv".format(work_dir, date_string), sep=";", header=None, index_col=False, parse_dates=[2])

        # for each row
        for k, row in data.iterrows():
            tag, media, data_ora = get_parameter_from_row(row) # AI = True because here we analise only ai files
            
            # If it is a different TAG
            if len(tags[tags["TAG_LIV"]==tag]["DENOMINAZIONE"].array) == 0:
                continue

            code, ambito, is_pozzo = get_base_info_tags(tags=tags, tag_liv=tag)

            index_portata = -1

            # This code could represent a "idrometro" or a "pozzo"
            if is_pozzo == 0:
                # Case "idrometro" 
                # TODO FIUME PO INSERT IN OTHER TABLE
                logging.info("Idrometro: %s", "{}".format(code))
                # TODO Here you can directly insert it into the database
                continue
            

            # Reading piano campagna
            piano_campagna = tags[tags["TAG_LIV"]==tag]["PIANO_CAMPAGNA"].array[0]

            # Is portata in file?
            is_portata_here = tags[tags["TAG_LIV"]==tag]["INFILE"].array[0]
            portata_tag = tags[tags["TAG_LIV"]==tag]["TAG_PORTATA"].array

            portata = 0


            # 1 is here, 0 is not here -1 does not exist
            if is_portata_here == 1:
                # Simple case, get the portata and then insert in in the db
                portata_empty = 0
                for sensor_tag in portata_tag:
                    # It is not possible to apply both filters at the same time
                    value = data[data[AI.index("TAG")] == sensor_tag] # filtering by tag 
                    value = value[value[AI.index("START_TS")] == data_ora] # filtering by time
                    
                    # keeping track of the portata index to delete
                    index_portata = value.index.values.astype(int)[0]

                    # This is used to check if there exist a corresponding portata value.
                    # If it does not exist the data will not be inserted
                    if value.empty:
                        portata_empty += 1

                    # here we can have multiple portata data, so we should sum it
                    portata += value[AI.index("MEAN")].array[0]
                
                if portata_empty == len(portata_tag):
                    portata = -1

            elif is_portata_here == 0:
                portata_tag = portata_tag[0] # For new sensor there exist only one tag
                
                # Least efficient solution: in this case we look in each file to find a valid row (valid row = right tag and data_ora)
                for file_name_portata in subset_file_list:
                    portata_data = pd.read_csv("{}/{}".format(work_dir, file_name_portata), sep=";", header=None, index_col=False, parse_dates=[2])


                    portata_data_filtered = portata_data[portata_data[DI.index("TAG")]==portata_tag] # filtering by tag 
                    portata_data_filtered = portata_data_filtered[portata_data_filtered[DI.index("START_TS")]==data_ora] # filtering by time
                    if portata_data_filtered.empty:
                       continue


                    # Debug
                    # print("portata of {}, {} found in {}, while source file is {}".format(code, data_ora, file_name_portata, file_name))
                    
                    portata = portata_data_filtered[DI.index("TIME1")].array[0]
                    

                    # Deleting data from csv
                    if delete_opt:
                        portata_data = portata_data.drop(portata_data_filtered.index.values.astype(int)[0], axis=0)
                        portata_data.to_csv("{}/{}".format(work_dir, file_name_portata), index=False, header=None,  sep=";")
                
                        
            else:
                print("No portata defined")
                continue
                
            portata = round(portata, 2)
            # Insert in db
            if piano_campagna > 0:
                real_level_value = round(media - piano_campagna,2)
            else:
                if media < 0:
                    real_level_value = round(media,2)
                else:
                    real_level_value = round(-media,2)
                
            logging.info("Pozzo: %s", "DATA ORD: {}, COD POZZO: {}, TAG: {}, MEDIA: {}, PIANO CAMPAGNA: {}, PORTATA: {}, REAL LEVEL VALUE: {}".format(data_ora, code, tag, media, piano_campagna, portata, real_level_value))
            dictionary["data_ora"].append(data_ora)
            dictionary["livello"].append(real_level_value)
            dictionary["portata"].append(portata)
            dictionary["cod_pozzo"].append(code)
            dictionary["ambito"].append(ambito)

            if index_portata != -1:
                index_list.append(index_portata)

            index_list.append(k)
            # print("INDEX: {}".format(row.index.values.astype(int)[0]))
            # print("OTHER INDEX {}".format(k))
            # print(data.iloc[k])
            # print(row)
            # print(dictionary)
            
            # Checking file age
            day_difference = now - date_level
            if day_difference.days > 7:
                # Delete file
                logging.info("File: %s", "{} too old deleting...".format(file_name))
        # print(index_list)
        
        if delete_opt:
            data = data.drop(index_list, axis=0)
            data.to_csv("{}/{}".format(work_dir, file_name), index=False, header=None, sep=";")
    print(dictionary)
    def_df = pd.DataFrame(data=dictionary)
    def_df.to_csv("out.csv", index=False,sep=";")      
            






if __name__ == '__main__':

    # TODO Do we need root permission?
    # if os.geteuid() != 0:
    #     exit("You need to have root privileges to run this script.\nPlease try again, this time using 'sudo'. Exiting.")
    
    parser = argparse.ArgumentParser(description="Data extractor")


    # TODO to define parameter
    parser.add_argument('-d', '--delete',
                        help='enabling parse and delete', type=bool, required=True)

    parser.add_argument('-p', '--path', metavar='<path>',
                        help='working dir (where all Hera files are collected)', type=str, required=True)

    args = parser.parse_args()
    
    main(args)