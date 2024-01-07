import pandas as pd 
import matplotlib.pyplot as plt
import os
import numpy as np
from utilities import load_object
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import cartopy.crs as ccrs
import cartopy.io.img_tiles as cimgt

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

for ak in ang_limits:
    if os.path.isfile("KDE_limits/" + ak + "_KDE_limits"):
        ang_limits[ak] = load_object("KDE_limits/" + ak + "_KDE_limits")

plane_classes = os.listdir("../OceanState/trajs")
marks = ["valid", "test", "train"] 
starts = ["LDZA"]

ends = {start: [] for start in starts} 

longs = {start: {mark: [] for mark in marks} for start in starts}
lats = {start: {mark: [] for mark in marks} for start in starts}
desti = {start: {mark: [] for mark in marks} for start in starts}

for plane_class in plane_classes: 

    for mark in marks:

        for first_part in starts:
            
            if not os.path.isdir("../OceanState/trajs/" + plane_class + "/" + mark + "/" + first_part + "/"):
                continue

            for filename_short in os.listdir("../OceanState/trajs/" + plane_class + "/" + mark + "/" + first_part + "/"):
                
                second_part = filename_short.replace(".csv", "").split("_")[-1]

                if len(ends[first_part]) > 0 and second_part not in ends[first_part]:
                    continue
 
                filename = "../OceanState/trajs/" + plane_class + "/" + mark + "/" + first_part + "/" + filename_short

                if not os.path.isfile(filename):
                    continue

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
dict_label_ang = dict()
dict_label_desti = dict()
dir_for_airport = dict()

for first_part in starts:

    xoffset[first_part] = dict()
    yoffset[first_part] = dict()
    ang[first_part] = dict()
    label_ang[first_part] = dict() 
    dict_label_ang[first_part] = dict()
    dict_label_desti[first_part] = dict()
    dir_for_airport[first_part] = dict()

    minix = 10000
    maxix = - 10000
    miniy = 10000
    maxiy = - 10000

    for mark in marks:
   
        for i in range(len(longs[first_part][mark])):
            
            minix = min(minix, min(longs[first_part][mark][i]))
            maxix = max(maxix, max(longs[first_part][mark][i]))
            miniy = min(miniy, min(lats[first_part][mark][i]))
            maxiy = max(maxiy, max(lats[first_part][mark][i]))
              
    plt.figure()
    ax = plt.gca()
    ax.set_aspect('equal', adjustable = 'box')

    '''
    proj = ccrs.PlateCarree()
    fig = plt.figure(figsize = (12, 6))
    # Draw main ax on top of which we will add windroses
    main_ax = fig.add_subplot(1, 1, 1, projection = proj)
    main_ax.set_extent([minix - 0.125, maxix + 0.125, miniy - 0.125, maxiy + 0.125], crs = proj)
    main_ax.gridlines(draw_labels = True)
    main_ax.coastlines()

    request = cimgt.OSM()
    main_ax.add_image(request, 12)
    '''

    for mark in marks:
   
        for i in range(len(longs[first_part][mark])):
            
            plt.plot(longs[first_part][mark][i], lats[first_part][mark][i])

    plt.show()
    plt.close()
    plt.figure()

    ax = plt.gca()
    ax.set_aspect('equal', adjustable = 'box')

    '''
    proj = ccrs.PlateCarree()
    fig = plt.figure(figsize = (12, 6))
    # Draw main ax on top of which we will add windroses
    main_ax = fig.add_subplot(1, 1, 1, projection = proj)
    main_ax.set_extent([minix - 0.125, maxix + 0.125, miniy - 0.125, maxiy + 0.125], crs = proj)
    main_ax.gridlines(draw_labels = True)
    main_ax.coastlines()

    request = cimgt.OSM()
    main_ax.add_image(request, 12)
    '''

    for mark in marks:
   
        for i in range(len(longs[first_part][mark])):
            
            plt.scatter(longs[first_part][mark][i][-1], lats[first_part][mark][i][-1])

    plt.show()
    plt.close()