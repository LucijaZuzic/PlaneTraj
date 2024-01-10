import os
import tarfile
import gzip
import shutil

for date_states in os.listdir("states"):
    for hour_states in os.listdir("states/" + date_states):
        for hour_files in os.listdir("states/" + date_states + "/" + hour_states):
            if ".tar" in hour_files:
                print(hour_files)
                tfl = tarfile.open("states/" + date_states + "/" + hour_states + "/" + hour_files)
                if not os.path.isdir("states/" + date_states + "/" + hour_states + "/extracted"):
                    os.makedirs("states/" + date_states + "/" + hour_states + "/extracted")
                    tfl.extractall("states/" + date_states + "/" + hour_states + "/extracted")
                    with gzip.open("states/" + date_states + "/" + hour_states + "/extracted/" + hour_files.replace("tar", "gz"), 'rb') as f_in:
                        with open("states/" + date_states + "/" + hour_states + "/extracted/" + hour_files.replace("tar", ""), 'wb') as f_out:
                            shutil.copyfileobj(f_in, f_out)