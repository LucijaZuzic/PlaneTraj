from traffic.data import eurofirs, opensky
switzerland_raw = opensky.history(
"2018-08-01 05:00", # UTC time by default
"2018-08-01 22:00",
bounds=eurofirs["LSAS"]
)

# https://opensky-network.org/data/data-tools#d1
# https://easychair.org/publications/paper/BXjT
# https://traffic-viz.github.io/index.html
# https://github.com/xoolive/traffic

# also try traja
# https://github.com/traja-team/traja
# https://traja.readthedocs.io/en/latest/index.html