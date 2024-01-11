import traffic.core 
from rich.pretty import pprint
from rich.console import Console
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import os 

console = Console() 
 
epoch_time = datetime(1970, 1, 1)
 
to_runway = dict()

for usable_traj_filename in os.listdir("usable_trajs"):
    if ".csv" not in usable_traj_filename:
        continue
    print(usable_traj_filename)

    pd_file = pd.read_csv("usable_trajs/" + usable_traj_filename, index_col = False)
    old_len = len(pd_file)
    pd_file = pd_file.dropna(subset = ["lon", "lat", "baroaltitude"]) 
    if len(pd_file) != old_len:
        continue
 
    callsign_array = []
    for cs in pd_file["callsign"]: 
        callsign_array.append(cs.strip())

    timestamps_array = []
    for ts in pd_file["time"]: 
        timestamps_array.append(traffic.core.time.to_datetime(ts))  

    altitudes_array = []
    for ba in pd_file["baroaltitude"]:
        feet = int(np.round(ba / 0.3048, 0))
        altitudes_array.append(feet)
  
    pd_file_new = pd.DataFrame() 
    pd_file_new["timestamp"] = timestamps_array
    pd_file_new["icao24"] = pd_file["icao24"]
    pd_file_new["latitude"] = pd_file["lat"]
    pd_file_new["longitude"] = pd_file["lon"]
    pd_file_new["groundspeed"] = pd_file["velocity"]
    pd_file_new["vertical_rate"] = pd_file["vertrate"]
    pd_file_new["callsign"] = callsign_array
    pd_file_new["altitude"] = altitudes_array
    pd_file_new["squawk"] = pd_file["squawk"]
  
    pd_file_new.to_pickle("usable_trajs/" + usable_traj_filename.replace(".csv", ".pkl")) 

    f = traffic.core.Flight.from_file("usable_trajs/" + usable_traj_filename.replace(".csv", ".pkl"))
    
    #print(f)
    #pprint(f)
    #console.print(f)
    #print(f.start, f.callsign, f.icao24, f.stop, f.squawk, f.distance())
    ta = f.takeoff_airport() 
    #print(ta)
    
    for el in f.takeoff_from_runway(ta):
        print(el)
        el.to_csv("mynew.csv")
        pd_el = pd.read_csv("mynew.csv")
        runway_nums = list(pd_el["runway"])
        print(runway_nums)
        os.remove("mynew.csv")

# https://opensky-network.org/data/data-tools#d1
# https://easychair.org/publications/paper/BXjT
# https://traffic-viz.github.io/index.html
# https://github.com/xoolive/traffic

# also try traja
# https://github.com/traja-team/traja
# https://traja.readthedocs.io/en/latest/index.html