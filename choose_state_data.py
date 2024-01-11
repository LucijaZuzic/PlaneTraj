import os
import pandas as pd 
from datetime import datetime, timedelta
import tarfile
import gzip
import shutil

epoch_time = datetime(1970, 1, 1)

state_files = set()
state_files_have = set()
all_trajs = set()
usable_trajs = set()
   
for file_name in os.listdir("usable_flights"):

    if "YSSY_YMML" not in file_name:
        continue

    pd_file = pd.read_csv("usable_flights/" + file_name, index_col = False)

    for ix in range(len(pd_file)):

        usable_traj = True

        cs = str(pd_file["callsign"][ix])
        while len(cs) < 8:
            cs += " "
        icao = pd_file["icao24"][ix]

        start_sec = pd_file["firstSeen"][ix]
        start_time = epoch_time + timedelta(seconds = int(start_sec))

        end_sec = pd_file["lastSeen"][ix]
        end_time = epoch_time + timedelta(seconds = int(end_sec))

        traj_name = cs + "_" + icao + "_" + str(start_sec) + "_" + str(end_sec)

        all_trajs.add(traj_name)

        #print(icao, cs, start_time, end_time, (end_time - start_time))

        start_hour = datetime(year = start_time.year, month = start_time.month, day = start_time.day, hour = start_time.hour)
        end_hour = datetime(year = end_time.year, month = end_time.month, day = end_time.day, hour = end_time.hour)

        #print(start_hour, end_hour)

        dt = start_hour

        while dt <= end_hour: 

            date_str = dt.strftime("%Y-%m-%d")
            hour_str = dt.strftime("%H") 
            name_of_file_with_data = "states/" + date_str + "/" + hour_str + "/states_" + date_str + "-" + hour_str + ".csv.tar"
             
            #print(name_of_file_with_data)

            state_files.add(name_of_file_with_data)

            if os.path.isfile(name_of_file_with_data):

                state_files_have.add(name_of_file_with_data)
  
            else:

                usable_traj = False

            dt += timedelta(hours = 1)

        if usable_traj:
            usable_trajs.add(traj_name)

print(len(state_files))
print(len(state_files_have))
print(len(all_trajs), len(usable_trajs))

if not os.path.isdir("usable_trajs"):
    os.makedirs("usable_trajs")
 
for file_name in os.listdir("usable_flights"):

    if "YSSY_YMML" not in file_name:
        continue
  
    pd_file = pd.read_csv("usable_flights/" + file_name, index_col = False)

    for ix in range(len(pd_file)):

        cs = str(pd_file["callsign"][ix])
        while len(cs) < 8:
            cs += " "
        icao = pd_file["icao24"][ix]

        start_sec = pd_file["firstSeen"][ix]
        start_time = epoch_time + timedelta(seconds = int(start_sec))

        end_sec = pd_file["lastSeen"][ix]
        end_time = epoch_time + timedelta(seconds = int(end_sec))

        traj_name = cs + "_" + icao + "_" + str(start_sec) + "_" + str(end_sec)

        if traj_name not in usable_trajs:
            continue

        if os.path.isfile("usable_trajs/" + traj_name + ".csv"):
            continue
  
        #print(icao, cs, start_time, end_time, (end_time - start_time))

        start_hour = datetime(year = start_time.year, month = start_time.month, day = start_time.day, hour = start_time.hour)
        end_hour = datetime(year = end_time.year, month = end_time.month, day = end_time.day, hour = end_time.hour)

        #print(start_hour, end_hour)

        dt = start_hour
  
        new_df = pd.DataFrame()

        while dt <= end_hour: 

            date_str = dt.strftime("%Y-%m-%d")
            hour_str = dt.strftime("%H") 
            name_of_file_with_data = "states/" + date_str + "/" + hour_str + "/states_" + date_str + "-" + hour_str + ".csv.tar"
             
            print(name_of_file_with_data)  

            os.makedirs("states/" + date_str + "/" + hour_str + "/extracted")
            tfl = tarfile.open(name_of_file_with_data)
            tfl.extractall("states/" + date_str + "/" + hour_str + "/extracted")
            with gzip.open("states/" + date_str + "/" + hour_str + "/extracted/states_" + date_str + "-" + hour_str + ".csv.gz") as f_in:
                with open("states/" + date_str + "/" + hour_str + "/states_" + date_str + "-" + hour_str + ".csv", 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            tfl.close()

            if os.path.isdir("states/" + date_str + "/" + hour_str + "/extracted"):
                for tf in os.listdir("states/" + date_str + "/" + hour_str + "/extracted"):
                    os.remove("states/" + date_str + "/" + hour_str + "/extracted/" + tf)
                os.rmdir("states/" + date_str + "/" + hour_str + "/extracted")

            name_of_file_pd = name_of_file_with_data.replace(".tar", "")

            if os.path.isfile(name_of_file_pd):
  
                file_with_data = pd.read_csv(name_of_file_pd, index_col = False)
                #print(len(file_with_data))
                file_with_data = file_with_data[file_with_data["time"] >= start_sec]
                #print(len(file_with_data))
                file_with_data = file_with_data[file_with_data["time"] <= end_sec]
                #print(len(file_with_data))
                file_with_data = file_with_data[file_with_data["icao24"] == pd_file["icao24"][ix]]
                #print(len(file_with_data))
                file_with_data = file_with_data[file_with_data["callsign"] == cs]
                #print(len(file_with_data)) 

                new_df = pd.concat([new_df, file_with_data])

            os.remove(name_of_file_pd)

            dt += timedelta(hours = 1)

        new_df.to_csv("usable_trajs/" + traj_name + ".csv", index = False)