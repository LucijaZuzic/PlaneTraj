import os 
import matplotlib.pyplot as plt
from traffic.core import Flight, Traffic
from datetime import timedelta
from traffic.data import airports
from cartes.crs import EPSG_3112  
from cartes.crs import valid_crs 
from sklearn.cluster import OPTICS
from sklearn.preprocessing import StandardScaler

print(str(valid_crs("Sydney, Australia")["auth_name"][0]) + "_" + str(valid_crs("Sydney, Australia")["code"][0]))

airport_sydney = airports["YSSY"]
print(airport_sydney.latitude, airport_sydney.longitude)
tpl_bounds = airport_sydney.bounds
print(tpl_bounds)
new_bounds = (airport_sydney.longitude - 0.5, airport_sydney.latitude - 0.5, airport_sydney.longitude + 0.5, airport_sydney.latitude + 0.5)
   
fix, ax = plt.subplots(subplot_kw = dict(projection = EPSG_3112()))
list_runways = []
labels_set = set()
all_flights = []
mintd = timedelta(seconds = 1000000)
maxtd = timedelta(seconds = 0)
num_flight = 0
for usable_traj_filename in os.listdir("usable_trajs")[:100]: 
    if "pkl" not in usable_traj_filename:
        continue 
    print(usable_traj_filename)
    f = Flight.from_file("usable_trajs/" + usable_traj_filename)
    f = f.inside_bbox(new_bounds)
    if f: 
         
        td = f.duration
        f = f.assign_id(name = str(num_flight))
        num_flight += 1
        maxtd = max(maxtd, td)
        mintd = min(mintd, td)
        all_flights.append(f) 

print(maxtd, mintd)
print(maxtd.total_seconds(), mintd.total_seconds())
print(maxtd.total_seconds() / 10, mintd.total_seconds() / 10)

tfc = Traffic.from_flights(all_flights) 
print(len(all_flights)) 
t_dbscan = tfc.clustering(
     nb_samples = int(maxtd.total_seconds()),
     projection = EPSG_3112(), 
     features = ["vertical_rate", "groundspeed", "x", "y"],
     clustering = OPTICS(),
     transform = StandardScaler(),
).fit_predict() 
print(t_dbscan.groupby(["cluster"]).agg({"flight_id": "nunique"}))