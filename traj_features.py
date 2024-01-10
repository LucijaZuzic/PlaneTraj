import pandas as pd 
import matplotlib.pyplot as plt
import os
import numpy as np
from utilities import load_object
from scipy import stats
import utm

def fit_rayleigh(arr_fit):
    rayleigh_args = stats.rayleigh.fit(arr_fit)
    print(rayleigh_args) 
    mini = min(arr_fit)
    maxi = max(arr_fit)
    rng = maxi - mini
    rng_vals = np.arange(0, rng + rayleigh_args[0], (rng + rayleigh_args[0]) / 100)
    rayleigh_fit = [x / (rayleigh_args[1] ** 2) * np.e ** (- x ** 2 / (2 * rayleigh_args[1] ** 2)) for x in rng_vals]
    rayleigh_fit_x = [x + rayleigh_args[0] + mini for x in rng_vals]
    return rayleigh_args, rayleigh_fit, rayleigh_fit_x
 
from convert_traj_to_boxes import get_fractal_dim_for_coords

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

plane_classes = os.listdir("trajs")
marks = ["valid"] 
starts = ["LDZA"]

ends = {start: [] for start in starts} 

longs = {start: {mark: [] for mark in marks} for start in starts}
lats = {start: {mark: [] for mark in marks} for start in starts}
alts = {start: {mark: [] for mark in marks} for start in starts}
desti = {start: {mark: [] for mark in marks} for start in starts}
dfroms = {start: {mark: [] for mark in marks} for start in starts}
times = {start: {mark: [] for mark in marks} for start in starts}

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

                pd_file = pd.read_csv(filename, index_col = False)

                pd_file['group'] = pd_file['timestep'].eq(0).cumsum()
                df = pd_file.groupby('group')
 
                for name, data in df:
                    if list(data["distance_from_dep"])[0] > 50000:
                        continue
                    longs[first_part][mark].append(list(data["lon"]))
                    lats[first_part][mark].append(list(data["lat"]))
                    alts[first_part][mark].append(list(data["baroaltitude"]))
                    desti[first_part][mark].append(list(data["toICAO"]))
                    dfroms[first_part][mark].append(list(data["distance_from_dep"]))
                    times[first_part][mark].append(list(data["time"]))
       
diff_dist = {start: {mark: [] for mark in marks} for start in starts}
straightness = {start: {mark: [] for mark in marks} for start in starts}
duration = {start: {mark: [] for mark in marks} for start in starts}
velocity = {start: {mark: [] for mark in marks} for start in starts}
fractal_dims = {start: {mark: [] for mark in marks} for start in starts}

diff_dist_xy = {start: {mark: [] for mark in marks} for start in starts}
straightness_xy = {start: {mark: [] for mark in marks} for start in starts}
velocity_xy = {start: {mark: [] for mark in marks} for start in starts}
fractal_dims_xy = {start: {mark: [] for mark in marks} for start in starts}

for first_part in starts:
   
    plt.figure()
    ax = plt.gca()
    ax.set_aspect('equal', adjustable = 'box')
  
    for mark in marks:
  
        for i in range(len(longs[first_part][mark])):

            utm_vals = []
            easting_val = []
            northing_val = []

            for j in range(len(longs[first_part][mark][i])):
                utm_val = utm.from_latlon(lats[first_part][mark][i][j], longs[first_part][mark][i][j])
                utm_vals.append(utm_val)
                easting_val.append(utm_val[0])
                northing_val.append(utm_val[1]) 

            times[first_part][mark][i] = [t - times[first_part][mark][i][0] for t in times[first_part][mark][i]]

            maxdist = len(dfroms[first_part][mark][i])

            while dfroms[first_part][mark][i][maxdist - 1] > 50000 and maxdist > 0:
                maxdist -= 1

            if maxdist == 1:
                continue
            
            #plt.plot(longs[first_part][mark][i][:maxdist], lats[first_part][mark][i][:maxdist])
 
            new_arr_dists = []
            new_arr_velocity = [] 
            new_arr_dists_xy = []
            new_arr_velocity_xy = [] 

            for j in range(maxdist):

                if j > 0:

                    x_offset_part = easting_val[j] - easting_val[j - 1]
                    y_offset_part = northing_val[j] - northing_val[j - 1]
                    z_offset_part = alts[first_part][mark][i][j] - alts[first_part][mark][i][j - 1] 
                    t_offset_part = (times[first_part][mark][i][j] - times[first_part][mark][i][j - 1]) / 3600
                    x_offset_part /= 1000
                    y_offset_part /= 1000
                    z_offset_part /= 1000

                    xy_offset_part = np.sqrt(x_offset_part ** 2 + y_offset_part ** 2)
                    xyz_offset_part = np.sqrt(xy_offset_part ** 2 + z_offset_part ** 2) 

                    new_arr_dists.append(xyz_offset_part)
                    new_arr_dists_xy.append(xy_offset_part)
                    new_arr_velocity.append(xyz_offset_part / t_offset_part)
                    new_arr_velocity_xy.append(xy_offset_part / t_offset_part)

            diff_dist[first_part][mark].append(sum(new_arr_dists))
            diff_dist_xy[first_part][mark].append(sum(new_arr_dists_xy))

            x_offset = easting_val[maxdist - 1] - easting_val[0]
            y_offset = northing_val[maxdist - 1] - northing_val[0]
            z_offset = alts[first_part][mark][i][maxdist - 1] - alts[first_part][mark][i][0] 
            x_offset /= 1000
            y_offset /= 1000
            z_offset /= 1000

            xy_offset = np.sqrt(x_offset ** 2 + y_offset ** 2)
            xyz_offset = np.sqrt(xy_offset ** 2 + z_offset ** 2)

            straightness[first_part][mark].append(sum(new_arr_dists) / xyz_offset)
            straightness_xy[first_part][mark].append(sum(new_arr_dists_xy) / xy_offset)

            duration[first_part][mark].append(times[first_part][mark][i][maxdist - 1])

            velocity[first_part][mark].append(np.average(new_arr_velocity))
            velocity_xy[first_part][mark].append(np.average(new_arr_velocity_xy))

            fractal_dims[first_part][mark].append(get_fractal_dim_for_coords(longs[first_part][mark][i][:maxdist], lats[first_part][mark][i][:maxdist], alts[first_part][mark][i][:maxdist]))  
            fractal_dims_xy[first_part][mark].append(get_fractal_dim_for_coords(longs[first_part][mark][i][:maxdist], lats[first_part][mark][i][:maxdist], [1 for x in alts[first_part][mark][i][:maxdist]])) 
 
    #plt.show()
    #plt.close()
  
    plt.title("Difusion distance")
    plt.hist(diff_dist[first_part][mark], density = True, bins = 100) 
    rayleigh_args, rayleigh_fit, rayleigh_fit_x = fit_rayleigh(diff_dist[first_part][mark])
    #plt.plot(rayleigh_fit_x, rayleigh_fit)
    print(np.quantile(diff_dist[first_part][mark], 0.05))
    print(np.quantile(diff_dist[first_part][mark], 0.5))
    print(np.quantile(diff_dist[first_part][mark], 0.95)) 
    plt.axvline(np.quantile(diff_dist[first_part][mark], 0.05))
    plt.axvline(np.quantile(diff_dist[first_part][mark], 0.5))
    plt.axvline(np.quantile(diff_dist[first_part][mark], 0.95)) 
    plt.show()
    plt.close()

    plt.title("Difusion distance xy")
    plt.hist(diff_dist_xy[first_part][mark], density = True, bins = 100) 
    rayleigh_args, rayleigh_fit, rayleigh_fit_x = fit_rayleigh(diff_dist_xy[first_part][mark])
    #plt.plot(rayleigh_fit_x, rayleigh_fit)
    print(np.quantile(diff_dist_xy[first_part][mark], 0.05))
    print(np.quantile(diff_dist_xy[first_part][mark], 0.5))
    print(np.quantile(diff_dist_xy[first_part][mark], 0.95)) 
    plt.axvline(np.quantile(diff_dist_xy[first_part][mark], 0.05))
    plt.axvline(np.quantile(diff_dist_xy[first_part][mark], 0.5))
    plt.axvline(np.quantile(diff_dist_xy[first_part][mark], 0.95)) 
    plt.show()
    plt.close()
  
    plt.title("Straightness")
    plt.hist(straightness[first_part][mark], density = True, bins = 100)  
    rayleigh_args, rayleigh_fit, rayleigh_fit_x = fit_rayleigh(straightness[first_part][mark])
    #plt.plot(rayleigh_fit_x, rayleigh_fit)
    print(np.quantile(straightness[first_part][mark], 0.05))
    print(np.quantile(straightness[first_part][mark], 0.5))
    print(np.quantile(straightness[first_part][mark], 0.95)) 
    plt.axvline(np.quantile(straightness[first_part][mark], 0.05))
    plt.axvline(np.quantile(straightness[first_part][mark], 0.5))
    plt.axvline(np.quantile(straightness[first_part][mark], 0.95)) 
    plt.show()
    plt.close()

    plt.title("Straightness xy")
    plt.hist(straightness_xy[first_part][mark], density = True, bins = 100)  
    rayleigh_args, rayleigh_fit, rayleigh_fit_x = fit_rayleigh(straightness_xy[first_part][mark])
    #plt.plot(rayleigh_fit_x, rayleigh_fit)
    print(np.quantile(straightness_xy[first_part][mark], 0.05))
    print(np.quantile(straightness_xy[first_part][mark], 0.5))
    print(np.quantile(straightness_xy[first_part][mark], 0.95)) 
    plt.axvline(np.quantile(straightness_xy[first_part][mark], 0.05))
    plt.axvline(np.quantile(straightness_xy[first_part][mark], 0.5))
    plt.axvline(np.quantile(straightness_xy[first_part][mark], 0.95)) 
    plt.show()
    plt.close()

    plt.title("Duration")
    plt.hist(duration[first_part][mark], density = True, bins = 100) 
    rayleigh_args, rayleigh_fit, rayleigh_fit_x = fit_rayleigh(duration[first_part][mark])
    #plt.plot(rayleigh_fit_x, rayleigh_fit)
    print(np.quantile(duration[first_part][mark], 0.05))
    print(np.quantile(duration[first_part][mark], 0.5))
    print(np.quantile(duration[first_part][mark], 0.95)) 
    plt.axvline(np.quantile(duration[first_part][mark], 0.05))
    plt.axvline(np.quantile(duration[first_part][mark], 0.5))
    plt.axvline(np.quantile(duration[first_part][mark], 0.95)) 
    plt.show()
 
    plt.title("Velocity")
    plt.hist(velocity[first_part][mark], density = True, bins = 100)  
    rayleigh_args, rayleigh_fit, rayleigh_fit_x = fit_rayleigh(velocity[first_part][mark])
    #plt.plot(rayleigh_fit_x, rayleigh_fit)
    print(np.quantile(velocity[first_part][mark], 0.05))
    print(np.quantile(velocity[first_part][mark], 0.5))
    print(np.quantile(velocity[first_part][mark], 0.95)) 
    plt.axvline(np.quantile(velocity[first_part][mark], 0.05))
    plt.axvline(np.quantile(velocity[first_part][mark], 0.5))
    plt.axvline(np.quantile(velocity[first_part][mark], 0.95)) 
    plt.show()

    plt.title("Velocity xy")
    plt.hist(velocity_xy[first_part][mark], density = True, bins = 100)  
    rayleigh_args, rayleigh_fit, rayleigh_fit_x = fit_rayleigh(velocity_xy[first_part][mark])
    #plt.plot(rayleigh_fit_x, rayleigh_fit)
    print(np.quantile(velocity_xy[first_part][mark], 0.05))
    print(np.quantile(velocity_xy[first_part][mark], 0.5))
    print(np.quantile(velocity_xy[first_part][mark], 0.95)) 
    plt.axvline(np.quantile(velocity_xy[first_part][mark], 0.05))
    plt.axvline(np.quantile(velocity_xy[first_part][mark], 0.5))
    plt.axvline(np.quantile(velocity_xy[first_part][mark], 0.95)) 
    plt.show()

    plt.title("Fractal dimension")
    plt.hist(fractal_dims[first_part][mark], density = True, bins = 100)  
    rayleigh_args, rayleigh_fit, rayleigh_fit_x = fit_rayleigh(fractal_dims[first_part][mark])
    #plt.plot(rayleigh_fit_x, rayleigh_fit)
    print(np.quantile(fractal_dims[first_part][mark], 0.05))
    print(np.quantile(fractal_dims[first_part][mark], 0.5))
    print(np.quantile(fractal_dims[first_part][mark], 0.95)) 
    plt.axvline(np.quantile(fractal_dims[first_part][mark], 0.05))
    plt.axvline(np.quantile(fractal_dims[first_part][mark], 0.5))
    plt.axvline(np.quantile(fractal_dims[first_part][mark], 0.95)) 
    plt.show()

    plt.title("Fractal dimension xy")
    plt.hist(fractal_dims_xy[first_part][mark], density = True, bins = 100)  
    rayleigh_args, rayleigh_fit, rayleigh_fit_x = fit_rayleigh(fractal_dims_xy[first_part][mark])
    #plt.plot(rayleigh_fit_x, rayleigh_fit)
    print(np.quantile(fractal_dims_xy[first_part][mark], 0.05))
    print(np.quantile(fractal_dims_xy[first_part][mark], 0.5))
    print(np.quantile(fractal_dims_xy[first_part][mark], 0.95)) 
    plt.axvline(np.quantile(fractal_dims_xy[first_part][mark], 0.05))
    plt.axvline(np.quantile(fractal_dims_xy[first_part][mark], 0.5))
    plt.axvline(np.quantile(fractal_dims_xy[first_part][mark], 0.95)) 
    plt.show()
 
    plt.figure()
    ax = plt.gca()
    ax.set_aspect('equal', adjustable = 'box')