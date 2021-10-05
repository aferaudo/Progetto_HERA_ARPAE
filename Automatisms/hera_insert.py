import os
import pandas as pd
from datetime import datetime, timedelta
import logging
import argparse



queries = [
    "INSERT INTO dbo.IDROMETRI_LIV (data_ora, livello, nome)(?,?,?)", # 0 = idrometro
    "(data_ora,livello,portata,cod_pozzo) values(?,?,?,?)" # 1 = pozzo
]


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


    



# This script should read the data in RWAIyyyymmddhhmmss.csv RWDIyyyymmddhhmmss.csv and insert it into a database.
# Next it has to call the script that computes the status (monitor/status_monitor.py)
# Once a file has been analysed, it will be maintaned for 5 days as backup

FORMAT = '%(levelname)s:%(asctime)-15s %(message)s'


# Logging configuration
logging.basicConfig(filename='automatism_hera.log', format=FORMAT, level=logging.DEBUG)

# formatting data_parser
d = lambda x : datetime.strptime(x, "%Y%m%d%H%M%S")

def main(argv):

    work_dir = argv.path
    file_list = os.listdir(work_dir)
    tags = pd.read_excel('pozzi_tags/Tag Pozzi con Sonde_per TLC_1.xlsx') # File useful for tag match
    subset_file_list = [name for name in file_list if "DI" in name]
    now = datetime.now() # This is used to understand which file should be deleted

    for file_name in file_list:

        # Filtering file name to get the datetime: used to determine file age
        date = datetime.strptime(file_name[4:18], "%Y%m%d%H%M%S")
        date_string = file_name[4:18] # This will be used to retrieve the corresponding file
        
        # Checking file age
        day_difference = now - date
        if day_difference.days > 5:
            # Delete file
            logging.info("File: %s", "{} too old deleting...".format(file_name))
        
        # These files will be read only for some kind of sensors
        if "DI" in file_name:
            print("File {} found, already opened".format(file_name))
            continue

        # TODO Only today's files should be analysed
        # if day_difference.days == 0:
        #     print("Ok")

        data = pd.read_csv("{}/{}".format(work_dir, file_name), sep=";", header=None, index_col=False, parse_dates=[2])
        
        # Efficient implementation
        # portata_data = pd.read_csv("{}/RWDI{}.csv".format(work_dir, date_string), sep=";", header=None, index_col=False, parse_dates=[2])

        for k, row in data.iterrows():
            tag, media, data_ora = get_parameter_from_row(row) # AI = True because here we analise only ai files
            
            if len(tags[tags["TAG_LIV"]==tag]["DENOMINAZIONE"].array) == 0:
                continue
            code = tags[tags["TAG_LIV"]==tag]["DENOMINAZIONE"].array[0] # transform the series in array and then get the first element ([0])


            # This code could represent a "idrometro" or a "pozzo"
            is_pozzo = tags[tags["TAG_LIV"]==tag]["TYPE"].array[0]
            
            if is_pozzo == 0:
                # Case "idrometro" 
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
                portata_empty = 0
                for sensor_tag in portata_tag:
                    # It is not possible to apply both filters at the same time
                    value = data[data[AI.index("TAG")] == sensor_tag] # filtering by tag 
                    value = value[value[AI.index("START_TS")] == data_ora] # filtering by time
                    
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
                
                # Use portata_data read from DI file
                for file_name_portata in subset_file_list:
                    portata_data = pd.read_csv("{}/{}".format(work_dir, file_name_portata), sep=";", header=None, index_col=False, parse_dates=[2])


                    portata_data_filtered = portata_data[portata_data[DI.index("TAG")]==portata_tag] # filtering by tag 
                    portata_data_filtered = portata_data_filtered[portata_data_filtered[DI.index("START_TS")]==data_ora] # filtering by time
                    if portata_data_filtered.empty:
                       continue
                    print("portata of {}, {} found in {}, while source file is {}".format(code, data_ora, file_name_portata, file_name))
                    portata = portata_data_filtered[DI.index("TIME1")].array[0]

                        
                

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

            # break

            # TODO FIUME PO INSERT IN OTHER TABLE
            






if __name__ == '__main__':

    # TODO Do we need root permission?
    # if os.geteuid() != 0:
    #     exit("You need to have root privileges to run this script.\nPlease try again, this time using 'sudo'. Exiting.")
    
    parser = argparse.ArgumentParser(description="Data extractor")


    # TODO to define parameter
    parser.add_argument('-p', '--path', metavar='<path>',
                        help='working dir (where all Hera files are collected)', type=str, required=True)

    args = parser.parse_args()
    
    main(args)