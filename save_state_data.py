
import requests
from bs4 import BeautifulSoup
from urllib.request import urlretrieve
import os
from datetime import datetime, timedelta
import opensky_api 

opensky = opensky_api.OpenSkyApi("lzuzic", "uGJp64kA") 
epoch_time = datetime(1970, 1, 1)

url_one = 'https://opensky-network.org/datasets/states/'
reqs_one = requests.get(url_one)
soup_one = BeautifulSoup(reqs_one.text, 'html.parser')
  
for link_one in soup_one.find_all('a'):
    link_one_href = link_one.get('href')
    if "2" in link_one_href:
        url_two = url_one + link_one_href[2:]
        
        for h in range(24):
            h_str = str(h)
            if len(h_str) == 1:
                h_str = "0" + h_str
            dir_to_save = "states_filtered/" + link_one_href[2:] + "/" + h_str
            filename_to_save = "states_" + link_one_href[2:] + "-" + h_str + ".csv.tar"

            file_csv_url = url_two + "/" + h_str + "/states_" + link_one_href[2:] + "-" + h_str + ".csv.tar"

            dt_start_frame = datetime.strptime(link_one_href[2:] + "-" + h_str, "%Y-%m-%d-%H")
            dt_end_frame = dt_start_frame + timedelta(hours = 1)


            start_sec = int((dt_start_frame - epoch_time).total_seconds())
            end_sec = int((dt_end_frame - epoch_time).total_seconds())

            data_res = opensky.get_departures_by_airport("LDZA", start_sec, end_sec)
            
            data_discovered = []
            if data_res != None:
                for e in data_res:  
                    dict_e = eval(str(e))  
                    if dict_e["estArrivalAirport"] == "EGLL":
                        data_discovered.append(dict_e)

            if len(data_discovered) > 0:

                print("Found", datetime.strftime(dt_start_frame, "%Y-%m-%d-%H"), datetime.strftime(dt_end_frame, "%Y-%m-%d-%H"))
                
                #if not os.path.isdir(dir_to_save):
                    #os.makedirs(dir_to_save)
                #else:
                    #continue

                #urlretrieve(file_csv_url, dir_to_save + "/" + filename_to_save)

            else:

                print("Nothing", datetime.strftime(dt_start_frame, "%Y-%m-%d-%H"), datetime.strftime(dt_end_frame, "%Y-%m-%d-%H"))