from datetime import datetime, timedelta
import os
import shutil 
import gzip

def download_weather(airport, datetime_obj):
  
    end_url = ".en.utf8.00000000.csv.gz"
     
    date_str = datetime_obj.strftime("%d.%m.%Y")
    month_str = datetime_obj.strftime("%m")
    if month_str[0] == "0":
        month_str = month_str[1:]
    day_str = datetime_obj.strftime("%d")
    if day_str[0] == "0":
        day_str = day_str[1:]

    start_of_filename = airport + "." + date_str + "." + date_str + ".1.0.0" 

    filename_to_save = start_of_filename + end_url 
    dir_to_save = "rp5/" + airport

    print(dir_to_save + "/" + filename_to_save)

    if os.path.isfile(dir_to_save + "/" + filename_to_save):
  
        with gzip.open(dir_to_save + "/" + filename_to_save, 'rb') as f_in:
            with open((dir_to_save + "/" + filename_to_save).replace(".gz", ""), 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)

        os.remove(dir_to_save + "/" + filename_to_save)
     
dt = datetime(day = 25, month = 5, year = 2020)
dt_end = datetime(day = 27, month = 6, year = 2022) 

epoch_time = datetime(1970, 1, 1)

while dt <= dt_end:
    download_weather("YMML", dt)
    download_weather("LDZA", dt)
    download_weather("YSSY", dt)
    dt = dt + timedelta(days = 7)
