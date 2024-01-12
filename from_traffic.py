from traffic.core import time, Flight 
import pandas as pd
import numpy as np
import os   
from cartes.crs import EPSG_3112, valid_crs 

print(str(valid_crs("Sydney, Australia")["auth_name"][0]) + "_" + str(valid_crs("Sydney, Australia")["code"][0]))
  
for usable_traj_filename in os.listdir("usable_trajs"):
    if ".csv" not in usable_traj_filename:
        continue
    if "_processed" in usable_traj_filename:
        continue

    print(usable_traj_filename)

    pd_file = pd.read_csv("usable_trajs/" + usable_traj_filename, index_col = False)
    old_len = len(pd_file)
    pd_file = pd_file.dropna(subset = ["lon", "lat", "baroaltitude"]) 
    if len(pd_file) != old_len:
        os.remove("usable_trajs/" + usable_traj_filename)
        continue 
 
    callsign_array = []
    for cs in pd_file["callsign"]: 
        callsign_array.append(cs.strip())

    timestamps_array = []
    for ts in pd_file["time"]: 
        timestamps_array.append(time.to_datetime(ts))  

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
    f = Flight.from_file("usable_trajs/" + usable_traj_filename.replace(".csv", ".pkl"))
    f = f.filter() 
    f = f.resample('10s')  
    f = f.compute_xy(projection = EPSG_3112()) 
    f.to_pickle("usable_trajs/" + usable_traj_filename.replace(".csv", ".pkl")) 
    f.to_csv("usable_trajs/" + usable_traj_filename.replace(".csv", "_processed.csv"))