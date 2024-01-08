import pandas as pd 
import matplotlib.pyplot as plt
import os
import numpy as np
from datetime import datetime, timedelta
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import LinearSVC, SVC, NuSVC 
from utilities import load_object

def actual_and_predicted_score(pred, act):

    predicted_for_actual = dict()
    actual_for_predicted = dict()

    for ix in range(len(pred)):

        actual_val = act[ix] 
        predicted_val = pred[ix]

        if actual_val not in predicted_for_actual:
            predicted_for_actual[actual_val] = dict()

        if predicted_val not in predicted_for_actual[actual_val]:
            predicted_for_actual[actual_val][predicted_val] = 0
        
        predicted_for_actual[actual_val][predicted_val] += 1

        if predicted_val not in actual_for_predicted:
            actual_for_predicted[predicted_val] = dict()

        if actual_val not in actual_for_predicted[predicted_val]:
            actual_for_predicted[predicted_val][actual_val] = 0

        actual_for_predicted[predicted_val][actual_val] += 1
    
    print(predicted_for_actual, actual_for_predicted)

def hash_str_for_learning(val_to_hash):
    
    hashed_val = 0

    for letter in val_to_hash:
        hashed_val = hashed_val * 100 + ord(letter)
  
    return hashed_val

epoch_time = datetime(1970, 1, 1)

ang_limits = dict()  
ang_limits["LDZA"] = [0, 13, 75, 115, 140, 165, 180, 215, 280, 318, 360]
ang_limits["EGLL"] = [0, 60, 150, 180, 210, 255, 340, 360]
ang_limits["EDDF"] = [0, 14, 40, 95, 115, 137, 165, 180, 230, 265, 285, 310, 347, 360]
ang_limits["EDDT"] = [0, 25, 35, 50, 70, 100, 141, 161, 200, 255, 295, 325, 360]
ang_limits["EDDM"] = [0, 8, 44, 72, 115, 161, 215, 265, 280, 300, 337, 360]
ang_limits["YSSY"] = [0, 44, 90, 123, 143, 159, 169, 200, 240, 320, 330, 340, 350, 360]
ang_limits["YMML"] = [0, 40, 60, 100, 151, 169, 200, 320, 345, 360]
ang_limits["KLAX"] = [0, 17, 75, 127, 162, 200, 270, 325, 342, 360]
ang_limits["KJFK"] = [0, 22, 55, 120, 150, 158, 167, 205, 216, 287, 320, 339, 360]

for ak in ang_limits:
    if os.path.isfile("KDE_limits/" + ak + "_KDE_limits"):
        ang_limits[ak] = load_object("KDE_limits/" + ak + "_KDE_limits")
 
plane_classes = os.listdir("trajs")
marks = ["valid", "test", "train"] 
starts = ["EGLL"]

ends = {start: [] for start in starts} 

longs = {start: {mark: [] for mark in marks} for start in starts}
lats = {start: {mark: [] for mark in marks} for start in starts}
desti = {start: {mark: [] for mark in marks} for start in starts}
plane_type = {start: {mark: [] for mark in marks} for start in starts}
datetime_marker = {start: {mark: [] for mark in marks} for start in starts}

training_cols = ["u", "v", "temp", "operator", "modeltype"]
training_data = {start: {mark: {colu: [] for colu in training_cols} for mark in marks} for start in starts}
 
for plane_class in plane_classes: 

    for mark in marks:

        for first_part in starts:
            
            if not os.path.isdir("trajs/" + plane_class + "/" + mark + "/" + first_part + "/"):
                continue

            for filename_short in os.listdir("trajs/" + plane_class + "/" + mark + "/" + first_part + "/"):
                
                second_part = filename_short.replace(".csv", "").split("_")[-1]

                if len(ends[first_part]) > 0 and second_part not in ends[first_part]:
                    continue
 
                filename = "trajs/" + plane_class + "/" + mark + "/" + first_part + "/" + filename_short

                if not os.path.isfile(filename):
                    continue

                pd_file = pd.read_csv(filename, index_col = False) 

                pd_file['group'] = pd_file['timestep'].eq(0).cumsum()
                df = pd_file.groupby('group')
 
                for name, data in df:
                    if list(data["distance_from_dep"])[0] > 20000:
                        continue
                    longs[first_part][mark].append(list(data["lon"]))
                    lats[first_part][mark].append(list(data["lat"]))
                    desti[first_part][mark].append(list(data["toICAO"]))
                    datetime_marker[first_part][mark].append(list(data["time"]))
                    plane_type[first_part][mark].append(list(data["plane_class"]))
                    for colu in training_cols:
                        training_data[first_part][mark][colu].append(list(data[colu]))

xoffset = dict()
yoffset = dict()
ang = dict()
X = dict()
label_ang = dict()  

predictions_RFC = dict()
predictions_LSVC = dict()
predictions_SVC = dict()
predictions_NuSVC = dict()

for first_part in starts:

    xoffset[first_part] = dict()
    yoffset[first_part] = dict()
    ang[first_part] = dict()
    X[first_part] = dict()
    label_ang[first_part] = dict()   

    for mark in marks:

        xoffset[first_part][mark] = [[] for i in range(len(longs[first_part][mark]))]
        yoffset[first_part][mark] = [[] for i in range(len(longs[first_part][mark]))]

        for i in range(len(xoffset[first_part][mark])):
            xoffset[first_part][mark][i] = [long - longs[first_part][mark][i][0] for long in longs[first_part][mark][i]]
            yoffset[first_part][mark][i] = [lat - lats[first_part][mark][i][0] for lat in lats[first_part][mark][i]]
 
        X[first_part][mark] = []  
        ang[first_part][mark] = []
        label_ang[first_part][mark] = []

        for i in range(len(xoffset[first_part][mark])): 

            X_vals = [hash_str_for_learning(first_part)] 
            X_vals.append(hash_str_for_learning(desti[first_part][mark][i][0]))
            X_vals.append(hash_str_for_learning(plane_type[first_part][mark][i][0])) 

            timedelta_curr = timedelta(seconds = datetime_marker[first_part][mark][i][0]) 
            datetime_curr = epoch_time + timedelta_curr 
            X_vals += [datetime_curr.day, datetime_curr.month, datetime_curr.year, datetime_curr.weekday()]
            X_vals += [datetime_curr.hour * 3600 + datetime_curr.minute * 60 + datetime_curr.second]
            
            for colu in training_cols:
                X_vals.append(training_data[first_part][mark][colu][i][0])
               
            X[first_part][mark].append(X_vals)

            ang_one = (360 + np.arctan2(yoffset[first_part][mark][i][-1], xoffset[first_part][mark][i][-1]) / np.pi * 180) % 360
            ang[first_part][mark].append(ang_one)
            for i in range(len(ang_limits[first_part]) - 1):
                if ang_one >= ang_limits[first_part][i] and ang_one < ang_limits[first_part][i + 1]:
                    label_ang[first_part][mark].append(i)
                    break

        X[first_part][mark] = np.array(X[first_part][mark])
        label_ang[first_part][mark] = np.array(label_ang[first_part][mark])

    mini_for_feat = dict()
    maxi_for_feat = dict()

    for ix in range(len(X[first_part]["train"])):
        for feat_ix in range(len(X[first_part]["train"][ix])):
            mini_for_feat[feat_ix] = X[first_part]["train"][ix][feat_ix]
            maxi_for_feat[feat_ix] = X[first_part]["train"][ix][feat_ix] 
        break

    for mrkr in marks:
        for ix in range(len(X[first_part][mrkr])):
            for feat_ix in range(len(X[first_part][mrkr][ix])):
                mini_for_feat[feat_ix] = min(mini_for_feat[feat_ix], X[first_part][mrkr][ix][feat_ix])
                maxi_for_feat[feat_ix] = max(maxi_for_feat[feat_ix], X[first_part][mrkr][ix][feat_ix])
        
    range_for_feat = dict()
    for feat_ix in maxi_for_feat:
        range_for_feat[feat_ix] = maxi_for_feat[feat_ix] - mini_for_feat[feat_ix]

    X_scaled = dict()
    X_scaled[first_part] = dict()
    for mrkr in marks:
        X_scaled[first_part][mrkr] = []
        for ix in range(len(X[first_part][mrkr])):
            X_scaled[first_part][mrkr].append([])
            for feat_ix in range(len(X[first_part][mrkr][ix])):
                nval = X[first_part][mrkr][ix][feat_ix] - mini_for_feat[feat_ix]
                if range_for_feat[feat_ix] > 0:
                    nval = (X[first_part][mrkr][ix][feat_ix] - mini_for_feat[feat_ix]) / range_for_feat[feat_ix]
                X_scaled[first_part][mrkr][ix].append(nval)
  
    RFC = RandomForestClassifier(class_weight = "balanced")
    RFC.fit(X[first_part]["train"], label_ang[first_part]["train"])

    LSVC = LinearSVC(dual = "auto", class_weight = "balanced")
    LSVC.fit(X[first_part]["train"], label_ang[first_part]["train"])

    SVCL = SVC(class_weight = "balanced")
    SVCL.fit(X[first_part]["train"], label_ang[first_part]["train"])

    #NuSVCL = NuSVC(class_weight = "balanced")
    #NuSVCL.fit(X[first_part]["train"], label_ang[first_part]["train"])

    predictions_RFC[first_part] = dict()
    predictions_LSVC[first_part] = dict()
    predictions_SVC[first_part] = dict()
    #predictions_NuSVC[first_part] = dict()
    
    print("RFC")

    for mark in ["test"]:

        predictions_RFC[first_part][mark] = RFC.predict(X[first_part][mark])

        #print(predictions_RFC[first_part][mark], label_ang[first_part][mark])

        print(first_part, mark, RFC.score(X[first_part][mark], label_ang[first_part][mark]))

        actual_and_predicted_score(predictions_RFC[first_part][mark], label_ang[first_part][mark])
        
    print("LSVC")

    for mark in ["test"]:

        predictions_LSVC[first_part][mark] = LSVC.predict(X[first_part][mark])

        #print(predictions_LSVC[first_part][mark], label_ang[first_part][mark])

        print(first_part, mark, LSVC.score(X[first_part][mark], label_ang[first_part][mark]))

        actual_and_predicted_score(predictions_LSVC[first_part][mark], label_ang[first_part][mark])
        
    print("SVC")

    for mark in ["test"]:

        predictions_SVC[first_part][mark] = SVCL.predict(X[first_part][mark])

        #print(predictions_SVC[first_part][mark], label_ang[first_part][mark]) 

        print(first_part, mark, SVCL.score(X[first_part][mark], label_ang[first_part][mark]))

        actual_and_predicted_score(predictions_SVC[first_part][mark], label_ang[first_part][mark])
        
    '''
    print("NuSVC")

    for mark in ["test"]:

        predictions_NuSVC[first_part][mark] = NuSVCL.predict(X[first_part][mark])

        #print(predictions_NuSVC[first_part][mark], label_ang[first_part][mark])

        print(first_part, mark, NuSVCL.score(X[first_part][mark], label_ang[first_part][mark]))

        actual_and_predicted_score(predictions_NuSVCL[first_part][mark], label_ang[first_part][mark])
    '''