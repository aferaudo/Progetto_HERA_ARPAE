import os
import argparse
import json
from collections import Counter
import pyodbc
import sys
import numpy as np
from datetime import date


# DB connection for linux server machine
conn = pyodbc.connect('Driver={/opt/microsoft/msodbcsql17/lib64/libmsodbcsql-17.7.so.2.1};'
                      'Server=localhost;'
                      'Database=Hera;'
                      'UID=SA;'
                      'PWD=disiDatabase!;')
cursor = conn.cursor()

# 0 = red
# 1 = yellow
# 2 = green
# colors_list = ["#ff7f7f", "#FFFF7F", "#7fbf7f"]
colors_list = ["#fc8d59", "#FFFF7F", "#91cf60"]

query_stato = "SELECT STATO, COD_POZZO FROM dbo.STATOPOZZI WHERE AMBITO="

query_insert_status = "INSERT INTO dbo.StatoPozzi (cod_pozzo,ambito,stato,threshold) VALUES(?,?,?,?)"


# !!! The comparison to verify if level is under a threshold is done on its daily average
# Dynamic map containing for each cod_pozzo its corresponding threshold
thresholds_map = dict() 



# ambito map
# TODO maybe that's still too static
ambito_map = {
    # "PIACENZA": "PC",
    # "PARMA": "PR",
    # "REGGIOEMILIA": "RE",
    "MODENA": "MO",
    "BOLOGNA": "BO",
    "FERRARA": "FE",
    "RAVENNA": "RA",
    "FORLICESENA": "FC",
    "RIMINI": "RN"
}

def get_query_total_records_per_day(city):
    query_total_records_per_day="SELECT COD_POZZO, COUNT(*) from (SELECT COD_POZZO, MIN(DATA_ORA) AS time FROM {} GROUP BY COD_POZZO, MONTH(DATA_ORA), DAY(DATA_ORA), YEAR(DATA_ORA)) SRC GROUP BY COD_POZZO".format(city) 
    return query_total_records_per_day

def get_query_last_year_recording(city):
    query_last_year_recording = "SELECT COD_POZZO, MAX(YEAR(DATA_ORA)) FROM {} GROUP BY COD_POZZO".format(city)
    return query_last_year_recording

def get_query_last_year(city):
    query_data_last_year = "SELECT * FROM {} B WHERE B.PORTATA <= 0.3 AND B.DATA_ORA > (SELECT MAX(DATEADD(year,-1,DATA_ORA)) FROM {} WHERE COD_POZZO = B.COD_POZZO) ORDER BY B.COD_POZZO, B.LIVELLO DESC".format(city,city)
    return query_data_last_year

def get_query_always(city):
    query_always = "SELECT * FROM {} B WHERE B.PORTATA <= 0.3 ORDER BY B.COD_POZZO, B.LIVELLO DESC".format(city)
    return query_always

def get_query_last_day_date(city):
    query_last_day_date = "SELECT COD_POZZO, MAX(DATA_ORA) FROM {} WHERE PORTATA <= 0.3 GROUP BY COD_POZZO".format(city)
    return query_last_day_date

def get_query_delete_old_status(city):
    query_delete_old_status = "DELETE FROM STATOPOZZI WHERE AMBITO='{}'".format(city)
    return query_delete_old_status

def from_tuple_list_to_dict(tuple_list):
    to_return = dict()
    for t in tuple_list:
        to_return[t[0]] = t[1]
    return to_return


def color_selection(query_result, weights):
    # TODO add weights (ponderate average)
    """
        This method returns the color of the network
    """
    
    # Amount of returned values
    total_values = len(query_result)
    total_weights = 0

    # Compute percentage
    percentages = Counter() # Empty counter
    for row in query_result:
        # row[0] = STATO
        # row[1] = COD_POZZO
        percentages[row[0]] += weights[row[1]] # * 1
        total_weights += weights[row[1]]

    if total_weights == 0:
        return colors_list[2]
    
    # The ratio is computed with the most common element
    ratio = percentages.most_common(1)[0][1]/total_weights
    # print(ratio)
    if ratio > 0.5:
        # print(percentages.most_common(1)[0][0])
        return colors_list[percentages.most_common(1)[0][0]]
    else:
        # When the probability is the same or there are too many reds status among them, 
        # the color is yellow
        return colors_list[1]
    

def compute_pozzo_status(values, last_dates):
    # Nel calcolo del percentile deve essere contato anche i dati con portata!=0 ?
    # Il minimo deve essere quello di sempre o quello nei dati selezionati?
    # Organizzale per codice pozzo
    # pozzi_status = {"cod_pozzo": status}
    # Possible status values: 0 (red), 1 (yellow), 2 (green)
    # pozzi = {("cod_pozzo": [registered levels in the year from the last value registered]}
    pozzi = dict()

    # { 'cod_pozzo': status (0,1,2)}
    pozzi_status = dict()

    for row in values:
        # row[0] datetime
        # row[1] livello
        # row[2] portata
        # row[3] cod_pozzo
        if not row[3] in pozzi.keys():
            pozzi[row[3]] = list()
        
        pozzi[row[3]].append((row[0],row[1]))
    
    # Date is the second element of the tuple
    date_index = 0
    # Level is the second element of the tuple
    level_index = 1

    # Once dict has been populated we can compute the percentile
    for cod_pozzo in pozzi.keys():
        
        # creating list of levels to compute the percentile
        levels = [x[level_index] for x in pozzi[cod_pozzo]]
        
        # Computing percentile
        thresholds_map[cod_pozzo] = np.percentile(np.array(levels), 25)
        
        # Computing pozzi status
        # 1. compute mean of the last day (or just last value assumed)
       
        # 1.1 filter levels by selecting the last recorded
        levels_last_recorded_day = [x[level_index] for x in pozzi[cod_pozzo] if x[date_index].date() == last_dates[cod_pozzo].date()]
        
        # 1.2 Computing the mean
        last_day_mean = round(np.mean(levels_last_recorded_day), 3)
    
        # 2. compute status pozzo
        
        # 2.1 find the minimum value in the last year (this is used to determine the red status)
        min_value_last_year = np.min(levels)
        
        print("Pozzo: {}, media ultimo giorno: {}, minimo di sempre: {}".format(cod_pozzo, last_day_mean, min_value_last_year))
        
        if last_day_mean == min_value_last_year:
            pozzi_status[cod_pozzo] = 0
        elif last_day_mean > thresholds_map[cod_pozzo]:
            pozzi_status[cod_pozzo] = 2
        else:
            pozzi_status[cod_pozzo] = 1
        
    return pozzi_status


def compute_weight(amount_of_records, last_years):
    # TODO if an element has less than one/two year of data, it should get weight=0
    # TODO Add other parameter to compute weights: e.g. how much is important an element
    """
        This method returns a dict containing cod_pozzo as key and its weight as value
        The resulting weights should be used to compute the color of an area.

        Weights computed as ratio between amount of records and max amount of records
        if last year of data recorded is too low (e.g. 2018) then weight = 0
    """
    records_max = max(amount_of_records, key=lambda x:x[1])

    # if last year of data recorded is too low (e.g. 2018) then weight = 0
    last_years = from_tuple_list_to_dict(last_years)
    todays_date = date.today()

    weight_dict = dict()
    for value in amount_of_records:
        if todays_date.year - last_years[value[0]] <= 1:
            weight_dict[value[0]] = round(value[1]/records_max[1], 3)
        else:
            weight_dict[value[0]] = 0

    return weight_dict


def main(argv):
    
    
    # Color map changing
    # Fetching current colors (colors.json file)
    with open(args.path) as f:
        data = json.load(f)
        print(data)
    
    
    # Query for ambiti
    # cursor.execute(get_query_ambito())
    # ambiti = cursor.fetchall()
    # # The dict is used to take the Ambito starting from cod_pozzo
    # ambiti_dict = dict()
    # for ambito in ambiti:
    #     ambiti_dict[ambito[0]] = ambito[1]
    # print(ambiti_dict)


    for key in ambito_map.keys():
        
        # Query for values in the last year
        cursor.execute(get_query_always(key))
        rows = cursor.fetchall()
        if len(rows) == 0:
            continue
        # Query for to obtain the date of the last value recorded
        cursor.execute(get_query_last_day_date(key))
        dates = cursor.fetchall()

        pozzi_status = compute_pozzo_status(values=rows,last_dates=from_tuple_list_to_dict(dates))
        print("Soglie pozzi: {}".format(thresholds_map))
        print("Stato pozzi {}: {}".format(key,pozzi_status))
        print()

        # Delete old_status
        print("Updating status...")
        cursor.execute(get_query_delete_old_status(city=key))
        cursor.commit()

        # Insert new status
        for cod_pozzo in pozzi_status.keys():
            cursor.execute(query_insert_status, cod_pozzo, key, pozzi_status[cod_pozzo], thresholds_map[cod_pozzo])
            cursor.commit()
        
        print("Status updated!")

        print("Computing weights...")
        cursor.execute(get_query_total_records_per_day(city=key))
        tot_records = cursor.fetchall()

        cursor.execute(get_query_last_year_recording(city=key))
        last_years = cursor.fetchall()
        
        weights = compute_weight(amount_of_records=tot_records, last_years=last_years)
        print(weights)
        print("Weights: done.")

        print("Loading new status from db...")
        query = "{}'{}'".format(query_stato, key)
        cursor.execute(query)
        print("Query: {}".format(query))
        query_results = cursor.fetchall()

        if len(query_results) == 0:
            continue

        print("Updating map colors...")

        color = color_selection(query_results, weights=weights)
        print("Selected color: {}".format(color))
    
        for i in range(len(data['colorList'])):
            if data['colorList'][i]['name'] == ambito_map[key]:
                data['colorList'][i]['color'] = color
        print("Colors updated!")
        # print(data['colorList'])
        print()
        print()

    # Writing results on colors.json
    print("Writing colors.json ...")
    with open(args.path, "w") as f:
        json.dump(data, f)
        
    
    
    cursor.close()
    print("Done.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Monitor RETI Acque HERA Arpae")

    parser.add_argument('-p', '--path', metavar='<path>',
                        help='path of the file "colors.json"', type=str, required=True)

    args = parser.parse_args()
    
    main(args)