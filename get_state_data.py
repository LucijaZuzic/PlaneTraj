
import requests
from bs4 import BeautifulSoup
from urllib.request import urlretrieve
import os

url_one = 'https://opensky-network.org/datasets/states/'
reqs_one = requests.get(url_one)
soup_one = BeautifulSoup(reqs_one.text, 'html.parser')
  
for link_one in soup_one.find_all('a'):
    link_one_href = link_one.get('href') 
    if "2" in link_one_href:
        url_two = url_one + link_one_href[2:]
        print(url_two)  
        for h in range(24):
            h_str = str(h)
            if len(h_str) == 1:
                h_str = "0" + h_str
            dir_to_save = "states/" + link_one_href[2:] + "/" + h_str
            filename_to_save = "states_" + link_one_href[2:] + "-" + h_str + ".csv.tar"
            filename_csv = "states_" + link_one_href[2:] + "-" + h_str + ".csv"
            if not os.path.isfile(dir_to_save + "/" + filename_csv):
                if not os.path.isdir(dir_to_save):
                    os.makedirs(dir_to_save)
            else:
                continue
            file_csv_url = url_two + "/" + h_str + "/states_" + link_one_href[2:] + "-" + h_str + ".csv.tar"
            print(file_csv_url)  
            print(dir_to_save + "/" + filename_to_save)  
            try:
                urlretrieve(file_csv_url, dir_to_save + "/" + filename_to_save)
            except:
                continue