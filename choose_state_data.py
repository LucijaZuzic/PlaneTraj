import os
import pandas as pd 
from datetime import datetime, timedelta

epoch_time = datetime(1970, 1, 1)
   
for file_name in os.listdir("usable_flights"):
    if "YMML_YSSY" not in file_name:
        continue
    pd_file = pd.read_csv("usable_flights/" + file_name, index_col = False)

    for ix in range(len(pd_file)):
        cs = pd_file["callsign"][ix]
        while len(cs) < 8:
            cs += " "
        icao = pd_file["icao24"][ix]

        start_sec = pd_file["firstSeen"][ix]
        start_time = epoch_time + timedelta(seconds = int(start_sec))

        end_sec = pd_file["lastSeen"][ix]
        end_time = epoch_time + timedelta(seconds = int(end_sec))

        print(icao, cs, start_time, end_time, (end_time - start_time))

        start_hour = datetime(year = start_time.year, month = start_time.month, day = start_time.day, hour = start_time.hour)
        end_hour = datetime(year = end_time.year, month = end_time.month, day = end_time.day, hour = end_time.hour)

        print(start_hour, end_hour)

        dt = start_hour

        while dt <= end_hour: 

            date_str = dt.strftime("%Y-%m-%d")
            hour_str = dt.strftime("%H") 
            name_of_file_with_data = "states/" + date_str + "/" + hour_str + "/extracted/states_" + date_str + "-" + hour_str + ".csv"
             
            print(name_of_file_with_data)

            if os.path.isfile(name_of_file_with_data):

                file_with_data = pd.read_csv(name_of_file_with_data, index_col = False)
                print(len(file_with_data))
                file_with_data = file_with_data[file_with_data["time"] >= start_sec]
                print(len(file_with_data))
                file_with_data = file_with_data[file_with_data["time"] <= end_sec]
                print(len(file_with_data))
                file_with_data = file_with_data[file_with_data["icao24"] == pd_file["icao24"][ix]]
                print(len(file_with_data))
                file_with_data = file_with_data[file_with_data["callsign"] == cs]
                print(len(file_with_data))

            dt += timedelta(hours = 1)