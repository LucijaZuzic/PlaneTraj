import opensky_api 
import pandas as pd
import os
from datetime import datetime, timedelta
  
def get_data(start_airport, end_airport):

    dt = datetime(day = 25, month = 5, year = 2020)
    dt_end = datetime(day = 27, month = 6, year = 2022) 

    epoch_time = datetime(1970, 1, 1)

    opensky = opensky_api.OpenSkyApi("lzuzic", "uGJp64kA") 

    flights_data_frame_conn = pd.DataFrame()
    flights_data_frame_all = pd.DataFrame()

    print(start_airport, end_airport)

    while dt <= dt_end:

        start_sec = int((dt - epoch_time).total_seconds())
        end_sec = start_sec + 24 * 3600 
        data_res = opensky.get_departures_by_airport(start_airport, start_sec, end_sec)
        
        if data_res != None:
            for e in data_res:  
                
                dict_e = eval(str(e)) 
                
                for key in dict_e:
                    dict_e[key] = [dict_e[key]]

                new_df = pd.DataFrame(dict_e)
                flights_data_frame_all = pd.concat([flights_data_frame_all, new_df]).drop_duplicates().reset_index(drop = True) 
                if dict_e["estArrivalAirport"] == [end_airport]:
                    flights_data_frame_conn = pd.concat([flights_data_frame_conn, new_df]).drop_duplicates().reset_index(drop = True) 
                
        dt = dt + timedelta(days = 7)

    if not os.path.isdir("usable_flights"):
        os.makedirs("usable_flights")

    print(len(flights_data_frame_conn)) 
    flights_data_frame_conn.to_csv("usable_flights/usable_flights_" + start_airport + "_" + end_airport + ".csv", index = False)
    print(len(flights_data_frame_all)) 
    flights_data_frame_all.to_csv("usable_flights/usable_flights_" + start_airport + ".csv", index = False)
 
get_data("YSSY", "YMML")
get_data("YMML", "YSSY") 