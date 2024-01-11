from traffic.core  import Traffic, Flight
from rich.pretty import pprint
from rich.console import Console
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import os

from traffic.data.samples import belevingsvlucht
print(belevingsvlucht)
pprint(belevingsvlucht)
console = Console()
console.print(belevingsvlucht)

belevingsvlucht.to_csv("useme.csv")


epoch_time = datetime(1970, 1, 1)

for usable_traj_filename in os.listdir("usable_trajs"):

    pd_file = pd.read_csv("usable_trajs/" + usable_traj_filename, index_col = False)
 
    callsign_array = []
    for cs in pd_file["callsign"]: 
        callsign_array.append(cs.strip())

    timestamps_array = []
    for ts in pd_file["time"]:
        dt = epoch_time + timedelta(seconds = ts)
        timestamps_array.append(dt.strftime("%Y-%m-%d %H:%M:%S+00:00"))

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
 
    pd_file_new.to_csv("usable_trajs/" + usable_traj_filename.replace(".csv", "_processed.csv"))

    f = Flight.from_file("usable_trajs/" + usable_traj_filename.replace(".csv", "_processed.csv"))
    print(f)
    pprint(f)
    console.print(f)

# https://opensky-network.org/data/data-tools#d1
# https://easychair.org/publications/paper/BXjT
# https://traffic-viz.github.io/index.html
# https://github.com/xoolive/traffic

# also try traja
# https://github.com/traja-team/traja
# https://traja.readthedocs.io/en/latest/index.html