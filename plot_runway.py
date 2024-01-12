import os 
import matplotlib.pyplot as plt
from traffic.core import Flight
from traffic.data import airports
from cartes.crs import EPSG_3112
from utilities import random_colors
import pandas as pd  

airport_sydney = airports["YSSY"]
print(airport_sydney.latitude, airport_sydney.longitude)
tpl_bounds = airport_sydney.bounds
print(tpl_bounds)
new_bounds = (airport_sydney.longitude - 0.1, airport_sydney.latitude - 0.1, airport_sydney.longitude + 0.1, airport_sydney.latitude + 0.1)
pd_runway = pd.read_csv("my_runway.csv")

all_runways = list(set(list(pd_runway["runway"])))
rcs = random_colors(len(all_runways))
color_runway = {str(all_runways[i]): rcs[i] for i in range(len(all_runways))} 
print(color_runway)

dict_runways = dict()
for ix in range(len(pd_runway)):
    dict_runways[pd_runway["flight"][ix]] = pd_runway["runway"][ix]
   
fix, ax = plt.subplots(subplot_kw = dict(projection = EPSG_3112()))
list_runways = []
labels_set = set() 

airport_sydney.plot(ax, labels = dict(fontsize = 11), zorder = 1)

for usable_traj_filename in os.listdir("usable_trajs"): 
    if "pkl" not in usable_traj_filename:
        continue 

    f = Flight.from_file("usable_trajs/" + usable_traj_filename)
    f = f.inside_bbox(new_bounds)
    if f:
        rw = dict_runways[usable_traj_filename.replace(".pkl", "")] 
        clr = color_runway[str(rw)] 
        if str(rw) != 'nan':
            zo = 3
        else:
            zo = 2
        if rw not in labels_set: 
            f.plot(ax, color = clr, label = rw, zorder = zo)
            labels_set.add(rw)
        else:
            f.plot(ax, color = clr, zorder = zo)
plt.legend()
plt.show()  