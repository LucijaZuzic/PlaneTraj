import os
import pandas as pd

dict_cols = dict()

order_wind = [
              'calm, no wind', 
              'variable wind direction', 
              'north',
              'north-northeast', 
              'north-east', 
              'east-northeast', 
              'east', 
              'east-southeast', 
              'south-east', 
              'south-southeast', 
              'south', 
              'south-southwest', 
              'south-west', 
              'west-southwest',
              'west', 
              'west-northwest',
              'north-west',  
              'north-northwest', 
            ]

def encode_wind(wind_str):
    wind_str = wind_str.replace("Wind blowing from the ", "").lower()
    ord_in_wind = order_wind.index(wind_str) 
    if ord_in_wind < 2:
        return ord_in_wind + 1
    else:
        return (ord_in_wind - 2) * 22.5

ok_cols = ["T", "P", "P0", "U", "Ff", "Td"]
not_ok_cols = ["W'W'", "WW", "c"]

for weather_airport in os.listdir("rp5"):

    if weather_airport != "LDZA":
        continue
    print(weather_airport)
  
    for weather_file in os.listdir("rp5/" + weather_airport):

        wf = pd.read_csv("rp5/" + weather_airport + "/" + weather_file, skiprows = range(0, 6), sep = ';')   

        for col in wf.columns:

            if "Local" in col:
                continue
            
            if "Unnamed" in col:
                continue

            if col not in dict_cols:
                dict_cols[col] = set()

            for val in wf[col]:
                if col == "DD" and str(val) != "nan":
                    dict_cols[col].add(encode_wind(val))
                else:
                    if "W" in col and str(val) != "nan":
                        #dict_cols[col].add(val)
                        dict_cols[col].add(val.lower().replace("smoke", "sm").replace("freezing (supercooled)", "fs").replace("partial (covering part of the aerodrome)", "pt").replace("patch", "pc").replace("ground", "gd").replace("mist", "m").replace("fog", "f").replace("in the vicinity", "v").replace("thunderstorm", "t").replace("shower", "sh").replace("heavy", "h").replace("light", "l").replace("snow", "sn").replace("drizzle", "d").replace("rain", "r"))
                    else:
                        if col == "c" and str(val) != "nan":
                            for substr_val in val.split(","):
                                for substr_val_next in substr_val.split(" "):
                                    dict_cols[col].add(substr_val_next.strip().lower())
                        else:    
                            if str(val) != "nan":
                                dict_cols[col].add(val)

for col in dict_cols:
 
    print(col)
    print(dict_cols[col]) 