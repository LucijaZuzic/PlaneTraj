import pandas as pd 
import matplotlib.pyplot as plt
import os
import numpy as np
from scipy.stats import gaussian_kde
from utilities import save_object, load_object

universal_limits  = range(361)

ang_limits = dict()
ang_limits["LDZA"] = [0, 13, 75, 115, 140, 165, 180, 215, 280, 318, 360]
ang_limits["EGLL"] = [0, 60, 150, 180, 210, 255, 340, 360]
ang_limits["EDDF"] = [0, 14, 40, 95, 115, 137, 165, 180, 230, 265, 285, 310, 347, 360]
ang_limits["EDDT"] = [0, 25, 35, 50, 70, 100, 141, 161, 200, 255, 295, 325, 360]
ang_limits["EDDM"] = [0, 8, 44, 72, 115, 161, 215, 265, 280, 300, 337, 360]
ang_limits["YSSY"] = [0, 44, 90, 123, 143, 159, 169, 200, 240, 320, 330, 340, 350, 360]
ang_limits["YMML"] = [0, 40, 60, 100, 151, 169, 200, 320, 345, 360]
ang_limits["KLAX"] = [0, 17, 75, 127, 162, 200, 270, 325, 342, 360]
ang_limits["KJFK"] = [0, 22, 55, 120, 150, 158, 167, 205, 216, 287, 320, 339, 360]
 
plane_classes = os.listdir("trajs")
marks = ["valid"] 
starts = ["EGLL"]

ends = {start: [] for start in starts} 

longs = {start: {mark: [] for mark in marks} for start in starts}
lats = {start: {mark: [] for mark in marks} for start in starts}
desti = {start: {mark: [] for mark in marks} for start in starts}

for plane_class in plane_classes: 

    for mark in marks:

        for first_part in starts:
            
            if not os.path.isdir("trajs/" + plane_class + "/" + mark + "/" + first_part + "/"):
                continue

            for filename_short in os.listdir("trajs/" + plane_class + "/" + mark + "/" + first_part + "/"):
                
                second_part = filename_short.replace(".csv", "").split("_")[-1]

                if len(ends[first_part]) > 0 and second_part not in ends[first_part]:
                    continue
 
                filename = "trajs/" + plane_class + "/" + mark + "/" + first_part + "/" + filename_short

                if not os.path.isfile(filename):
                    continue

                #print(filename)

                pd_file = pd.read_csv(filename, index_col = False)

                pd_file['group'] = pd_file['timestep'].eq(0).cumsum()
                df = pd_file.groupby('group')
 
                for name, data in df: 
                    if list(data["distance_from_dep"])[0] > 20000:
                        continue
                    longs[first_part][mark].append(list(data["lon"]))
                    lats[first_part][mark].append(list(data["lat"]))
                    desti[first_part][mark].append(list(data["toICAO"]))

xoffset = dict()
yoffset = dict()
ang = dict()
label_ang = dict()  

for first_part in starts:

    xoffset[first_part] = dict()
    yoffset[first_part] = dict()
    ang[first_part] = dict()
    label_ang[first_part] = dict()  

    for mark in marks:

        xoffset[first_part][mark] = [[] for i in range(len(longs[first_part][mark]))]
        yoffset[first_part][mark] = [[] for i in range(len(longs[first_part][mark]))]

        for i in range(len(xoffset[first_part][mark])):
            xoffset[first_part][mark][i] = [long - longs[first_part][mark][i][0] for long in longs[first_part][mark][i]]
            yoffset[first_part][mark][i] = [lat - lats[first_part][mark][i][0] for lat in lats[first_part][mark][i]]
 
        X = [] 
        Y = []
        ang[first_part][mark] = []
        label_ang[first_part][mark] = []

        for i in range(len(xoffset[first_part][mark])):
            X.append([xoffset[first_part][mark][i][-1], yoffset[first_part][mark][i][-1]]) 
            Y.append(desti[first_part][mark][i][0])
            ang_one = (360 + np.arctan2(yoffset[first_part][mark][i][-1], xoffset[first_part][mark][i][-1]) / np.pi * 180) % 360
            ang[first_part][mark].append(ang_one)
            for i in range(len(universal_limits) - 1):
                if ang_one >= universal_limits[i] and ang_one < universal_limits[i + 1]:
                    label_ang[first_part][mark].append(i)
                    break

    all_together = []
    all_stacked = []
    count_of_label = [0 for val in range(360)]

    for mark in marks:
        all_stacked.append(ang[first_part][mark])
        for val in ang[first_part][mark]:
            all_together.append(val)
        for val in label_ang[first_part][mark]:        
            count_of_label[val] += 1
     
    sgn_label = [count_of_label[i] < count_of_label[i + 1] for i in range(359)] 

    infl_point = []
    mini_point = [0]

    for i in range(358):
        if sgn_label[i] != sgn_label[i + 1]:
            infl_point.append(i + 1)
            if sgn_label[i] == False and sgn_label[i + 1] == True:
                mini_point.append(i + 1)

    mini_point.append(360)

    if not os.path.isdir("local_min"):
        os.makedirs("local_min")
                    
    save_object("local_min/" + first_part + "_local_mins", mini_point)

    print(infl_point)
    print(mini_point)
    plt.title(first_part)
    plt.hist(all_stacked, bins = 360, stacked = True)

    for val in mini_point:
        plt.axvline(val)
  
    plt.show()
    plt.close()
    
    plt.title(first_part)
    plt.hist(all_stacked, bins = mini_point, stacked = True)
    plt.show()
    plt.close() 