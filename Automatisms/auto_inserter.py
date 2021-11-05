import os
import argparse
import pandas as pd
from datetime import datetime
from parser_hera import ParserHera
import timeit
import logging
# from db_utility import DbManager
import destroyer

# Logging configuration
FORMAT = '%(levelname)s:%(asctime)-15s %(message)s'


def main(argv):

    work_dir = argv.path
    logging.basicConfig(filename='automatism_hera.log', format=FORMAT, level=argv.log_level)
    logging.info("Parsing...")

    tags = pd.read_excel('pozzi_tags/Tag Pozzi con Sonde_per TLC_1.xlsx') # File useful for tag match

    # Entering in working dir
    os.chdir(work_dir)

    # listing working dir
    file_list = os.listdir(".")
    file_list.sort()
    
    subset_file_list_level = [name for name in file_list if "AI" in name]
    subset_file_list_portata = [name for name in file_list if "DI" in name]
    
    start = timeit.default_timer()

    parser = ParserHera(tags, subset_file_list_level, subset_file_list_portata)
    df_pozzi, df_idro = parser.parse()
    stop = timeit.default_timer()

    print(df_pozzi)
    print(df_idro)
    
    logging.info('Total parsing time: %s', str(stop - start)) 
    

    logging.info('Insert into db...')
    # Connect to db
    # db_manager = DbManager()
    # db_manager.insert_pozzi(df_pozzi)
    # db_manager.insert_idro_level(df_idro)
    logging.info('Done')

    if argv.delete:
        logging.info('Destroying...')
        destroyer.destroy_hera(file_list, days_ai=argv.daysAI, days_di=argv.daysDI)
        logging.info('Done')




if __name__ == '__main__':

    # TODO Do we need root permission?
    # if os.geteuid() != 0:
    #     exit("You need to have root privileges to run this script.\nPlease try again, this time using 'sudo'. Exiting.")
    
    parser = argparse.ArgumentParser(description="Data extractor")

    parser.add_argument('-p', '--path', metavar='<path>',
                        help='working dir (where all Hera files are collected)', type=str, required=True)
    
    parser.add_argument('-v', '--verbose', 
                        help="Print in automatism_hera.log all debug statements",
                        action="store_const", dest="log_level", const=logging.DEBUG,
                        default=logging.INFO)
    
    parser.add_argument('-d', '--delete',
                        help='enabling parse and delete', action='store_true', required=False, default=False)
    
    parser.add_argument('-dAI', '--daysAI', metavar='<num_days>',
                        help='days threshold for AI files default value 4', type=int, action=destroyer.DeleteAction, required=False, default=4)
    parser.add_argument('-dDI', '--daysDI', metavar='<num_days>',
                        help='days threshold for DI files default value 6', type=int, action=destroyer.DeleteAction, required=False, default=6)


    args = parser.parse_args()
    
    main(args)