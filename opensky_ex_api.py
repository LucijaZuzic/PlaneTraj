import opensky_api 
from datetime import datetime, timedelta
dt = datetime(day = 8, month = 10, year = 2023)
dt_end = datetime(day = 8, month = 1, year = 2024)
epoch_time = datetime(1970, 1, 1)

found = False
opensky = opensky_api.OpenSkyApi("lzuzic", "uGJp64kA") 
while dt < dt_end:
    start_sec = int((dt - epoch_time).total_seconds())
    end_sec = start_sec + 24 * 3600
    data_res = opensky.get_departures_by_airport("EGLL", start_sec, end_sec)
    #print(data_res)
    
    if data_res != None:
        #print(data_res)
        for e in data_res:  
            dict_e = eval(str(e)) 
            print(dict_e["estArrivalAirport"])
            if dict_e["estArrivalAirport"] == "EGLL":
                found = True
                break 
            #data_track = opensky.get_track_by_aircraft(dict_e["icao24"], start_sec)
            #print(data_track) 
    dt = dt + timedelta(days = 1)
    print(dt)