import os
import pandas as pd  
  
state_files = set()
state_files_have = set()
all_trajs = set()
usable_trajs = set()
   
for file_name in os.listdir("usable_flights"): 

    pd_file = pd.read_csv("usable_flights/" + file_name, index_col = False)
 
    cs_series = []

    for ix in range(len(pd_file)):

        usable_traj = True

        cs = str(pd_file["callsign"][ix])

        while len(cs) < 8:
            cs += " "

        if "nan" in cs:
            cs = ""

        cs_series.append(cs)

    pd_file["callsign"] = cs_series

    pd_file.to_csv("usable_flights/" + file_name, index = False)
            