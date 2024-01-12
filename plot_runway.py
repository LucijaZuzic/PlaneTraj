import pandas as pd 
import os 
import matplotlib.pyplot as plt
 
for usable_traj_filename in os.listdir("usable_trajs"):
    if ".csv" not in usable_traj_filename:
        continue
    if "_processed" not in usable_traj_filename:
        continue
    print(usable_traj_filename)

    pd_file = pd.read_csv("usable_trajs/" + usable_traj_filename, index_col = False)
    
    x = pd_file["x"]
    y = pd_file["y"]

    plt.figure()
    plt.plot(x, y)

    plt.show() 
    break  
