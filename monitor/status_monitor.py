import os
import argparse
import json
from collections import Counter
import pyodbc
import math
import sys


# DB connection for linux server machine
conn = pyodbc.connect('Driver={/opt/microsoft/msodbcsql17/lib64/libmsodbcsql-17.7.so.2.1};'
                      'Server=localhost;'
                      'Database=Hera;'
                      'UID=SA;'
                      'PWD=ServerVMHeraDB1*;')
cursor = conn.cursor()

# 0 = red
# 1 = yellow
# 2 = green
colors_list = ["#ff7f7f", "#FFFF7F", "#7fbf7f"]

# This method returns the color of the network
def color_selection(rows):
    
    # Amount of returned values
    total_values = len(rows)
    
    # Compute percentage
    percentages = Counter() # Empty counter
    for row in rows:
        percentages[row[0]] += 1
    
    # The ratio is computed with the most common element
    ratio = percentages.most_common(1)[0][1]/total_values
    if ratio > 0.5:
        return colors_list[percentages.most_common(1)[0][0]]
    else:
        # When the probability is the same or there are too many reds status among them, 
        # the color is yellow
        return colors_list[1]
    


# TODO
# This map establishes the single pozzo status
# Map creation should be dynamic:
# Read data from db and compute the "percentile 75" everything over is green, 
# values between it and minimum are orange and values under minimum are red! 
thresholds_map = dict()

# province map
province_map = {
    "PIACENZA": "PC",
    "PARMA": "PR",
    "REGGIOEMILIA": "RE",
    "MODENA": "MO",
    "BOLOGNA": "BO",
    "FERRARA": "FE",
    "RAVENNA": "RA",
    "FORLICESENA": "FC",
    "RIMINI": "RN"
}

common_query = "SELECT STATO FROM dbo.STATOPOZZI WHERE RETE="

def main(argv):
    
    
    # Color map changing
    # Fetching current colors (colors.json file)
    with open(args.path) as f:
        data = json.load(f)
        print(data)
    
    # Load values from db
    for key in province_map.keys():
        query = "{}'{}'".format(common_query, key)
        cursor.execute(query)
        print("Query: {}".format(query))
        rows = cursor.fetchall()

        if len(rows) == 0:
            continue

        color = color_selection(rows)
        print("Selected color: {}".format(color))
        data['province'][province_map[key]] = color

        
    # Writing results on colors.json
    with open(args.path, "w") as f:
        json.dump(data, f)
    
    
    cursor.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Monitor RETI Acque HERA Arpae")

    parser.add_argument('-p', '--path', metavar='<path>',
                        help='path of the file "colors.json"', type=str, required=True)

    args = parser.parse_args()
    
    main(args)