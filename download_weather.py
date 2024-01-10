import requests 
from datetime import datetime, timedelta
import os
import shutil
import requests
import gzip

def download_weather(airport, datetime_obj):

    start_url = "https://ru1.rp5.ru/download/files.metar/" 

    end_url = ".en.utf8.00000000.csv.gz"
    headers_use = {
        #GET /download/files.metar/YM/YMML.26.09.2013.26.09.2013.1.0.0.en.utf8.00000000.csv.gz HTTP/1.1
        "Accept": "text/html,application/xhtml+xml, application/xml;q=0.9, image/avif, image/webp,image/apng, */*;q=0.8, application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "hr-HR,hr;q=0.9,en-GB;q=0.8,en-US;q=0.7,en;q=0.6",
        "Connection": "keep-alive",
        "Cookie": "__gads=ID=7ca2653d635975dd:T=1704895671:RT=1704895671:S=ALNI_Mb0a1WADI_xRQkN58VyLrhnttXOkg; __gpi=UID=00000d3f231335e1:T=1704895671:RT=1704895671:S=ALNI_MZkwld_s0cPwBr0RT_QgPP4bB7wew",
        "Host": "ru1.rp5.ru",
        "Referer": "https://rp5.ru/",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "sec-ch-ua": '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "Windows" 
    }
 
    date_str = datetime_obj.strftime("%d.%m.%Y")
    month_str = datetime_obj.strftime("%m")
    if month_str[0] == "0":
        month_str = month_str[1:]
    day_str = datetime_obj.strftime("%d")
    if day_str[0] == "0":
        day_str = day_str[1:]

    start_of_filename = airport + "." + date_str + "." + date_str + ".1.0.0" 

    filename_to_save = start_of_filename + end_url

    mid_url = airport[:2] + "/" + start_of_filename

    url = start_url + mid_url + end_url
  
    dir_to_save = "rp5/" + airport

    if not os.path.isfile(dir_to_save + "/" + filename_to_save):

        if not os.path.isdir("rp5/" + airport):
            os.makedirs("rp5/" + airport) 

        respo = requests.get(url, headers = headers_use)

        print(respo.content)

        with open(dir_to_save + "/" + filename_to_save, 'wb') as out_file:
            shutil.copyfileobj(respo.raw, out_file)

        print('The file', dir_to_save + "/" + filename_to_save, 'was saved successfully')

    with gzip.open(dir_to_save + "/" + filename_to_save, 'rb') as f_in:
        with open((dir_to_save + "/" + filename_to_save).replace(".gz", ""), 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
     
dt = datetime(day = 25, month = 5, year = 2020)
dt_end = datetime(day = 27, month = 6, year = 2022) 

epoch_time = datetime(1970, 1, 1)

while dt <= dt_end:
    download_weather("YMML", dt)
    dt = dt + timedelta(days = 7)
    break
