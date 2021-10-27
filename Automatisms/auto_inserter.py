import os
import argparse
import pandas as pd
from datetime import datetime
from parser_hera import ParserHera
import timeit


def main(argv):

    work_dir = argv.path
    delete_opt = argv.delete

    tags = pd.read_excel('pozzi_tags/Tag Pozzi con Sonde_per TLC_1.xlsx') # File useful for tag match

    # Entering in working dir
    os.chdir(work_dir)

    # listing working dir
    file_list = os.listdir(".")

    subset_file_list_level = [name for name in file_list if "AI" in name]
    subset_file_list_portata = [name for name in file_list if "DI" in name]
    
    # now = datetime.now() # This is used to understand which file should be deleted
    

    start = timeit.default_timer()




    parser = ParserHera(tags, subset_file_list_level, subset_file_list_portata)

    df_pozzi, df_idro = parser.parse()
    df_pozzi.to_csv("../test/processed_pozzi.csv", index=False, header=None,  sep=";")
    df_idro.to_csv("../test/processed_idro.csv", index=False, header=None,  sep=";")
    stop = timeit.default_timer()

    print('Processing time: ', stop - start) 
    # print(df_pozzi)
    # print(df_idro)
    # Filtering file name to get the datetime: used to determine file age
    # datetime_file_name_level = datetime.strptime(file_name_level[4:18], "%Y%m%d%H%M%S")



if __name__ == '__main__':

    # TODO Do we need root permission?
    # if os.geteuid() != 0:
    #     exit("You need to have root privileges to run this script.\nPlease try again, this time using 'sudo'. Exiting.")
    
    parser = argparse.ArgumentParser(description="Data extractor")


    # TODO to define parameter
    parser.add_argument('-d', '--delete',
                        help='enabling parse and delete', type=bool, required=False)

    parser.add_argument('-p', '--path', metavar='<path>',
                        help='working dir (where all Hera files are collected)', type=str, required=True)

    args = parser.parse_args()
    
    main(args)