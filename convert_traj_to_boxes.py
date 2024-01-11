import numpy as np
import matplotlib.pyplot as plt 
from FractalDimension import fractal_dimension
import os
import pandas as pd
import utm
 
#mini_dim = 10 ** -1
#maxi_dim = 1
#step_size = 10 ** -1

def get_boxes(x_coords, y_coords, z_coords):

    x_min = min(x_coords)
    x_max = max(x_coords)
    x_range = x_max - x_min

    y_min = min(y_coords)
    y_max = max(y_coords)
    y_range = y_max - y_min

    z_min = min(z_coords)
    z_max = max(z_coords)
    z_range = z_max - z_min

    box_size = max(max(x_range, y_range), z_range) / 100
  
    used_boxes = set()

    total_len = 0  

    min_box_x = 1000000
    min_box_y = 1000000
    min_box_z = 1000000
    max_box_x = -1000000
    max_box_y = -1000000
    max_box_z = -1000000
 
    for p in range(len(x_coords) - 1):

        px = x_coords[p]
        py = y_coords[p]
        pz = z_coords[p] 

        px_next = x_coords[p + 1]
        py_next = y_coords[p + 1]
        pz_next = z_coords[p + 1] 

        box_end = (int(px_next // box_size), int(py_next // box_size), int(pz_next // box_size))

        x_boxes_offset = abs(px_next - px)
        y_boxes_offset = abs(py_next - py)
        z_boxes_offset = abs(pz_next - pz)

        max_offset = np.sqrt(np.sqrt(x_boxes_offset ** 2 + y_boxes_offset ** 2) + z_boxes_offset ** 2)

        if max_offset == 0:
            used_boxes.add(box_end)
            continue

        num_steps = np.ceil(max_offset / box_size * 4)
 
        x_dir = x_boxes_offset / num_steps
        y_dir = y_boxes_offset / num_steps
        z_dir = z_boxes_offset / num_steps
        
        if px_next < px:
            x_dir *= -1

        if py_next < py:
            y_dir *= -1

        if pz_next < pz:
            z_dir *= -1

        x_box_curr = px
        y_box_curr = py
        z_box_curr = pz 
            
        while True: 
            box_curr = (int(x_box_curr // box_size), int(y_box_curr // box_size), int(z_box_curr // box_size)) 
            used_boxes.add(box_curr)
            min_box_x = min(min_box_x, box_curr[0])
            min_box_y = min(min_box_y, box_curr[1])
            min_box_z = min(min_box_z, box_curr[2])
            max_box_x = max(max_box_x, box_curr[0])
            max_box_y = max(max_box_y, box_curr[1])
            max_box_z = max(max_box_z, box_curr[2])
            total_len += np.sqrt(np.sqrt(x_dir ** 2 + y_dir ** 2) + z_dir ** 2)
            if box_curr == box_end:
                break
            x_box_curr += x_dir
            y_box_curr += y_dir
            z_box_curr += z_dir
      
    '''
    fig = plt.figure()
    ax = plt.axes(projection='3d') 
 
    rising = [bs for bs in box_starts]
    for v1 in box_starts:
        const_v1 = [v1 for bs in box_starts]
        for v2 in box_starts:
            const_v2 = [v2 for bs in box_starts]
            plt.plot(const_v1, const_v2, zs = rising, color = "blue")
            plt.plot(const_v1, rising, zs = const_v2, color = "green")
            plt.plot(rising, const_v1, zs = const_v2, color = "yellow")
        
    for box in used_boxes:

        x_min_val, y_min_val, z_min_val = box
        x_min_val, y_min_val, z_min_val = x_min_val * box_size, y_min_val * box_size, z_min_val * box_size
        x_max_val, y_max_val, z_max_val = x_min_val + box_size, y_min_val + box_size, z_min_val + box_size

        x_range = np.arange(x_min_val, x_max_val + box_size / 10, box_size / 10)[:11]
        x_min_const = [x_min_val for x in x_range]
        x_max_const = [x_max_val for x in x_range] 

        y_range = np.arange(y_min_val, y_max_val + box_size / 10, box_size / 10)[:11]
        y_min_const = [y_min_val for y in y_range]
        y_max_const = [y_max_val for y in y_range]

        z_range = np.arange(z_min_val, z_max_val + box_size / 10, box_size / 10)[:11]
        z_min_const = [z_min_val for z in z_range]
        z_max_const = [z_max_val for z in z_range]

        plt.plot(x_min_const, y_min_const, zs = z_range, color = "blue")
        plt.plot(x_min_const, y_max_const, zs = z_range, color = "blue")
        plt.plot(x_max_const, y_min_const, zs = z_range, color = "blue")
        plt.plot(x_max_const, y_max_const, zs = z_range, color = "blue")

        plt.plot(x_min_const, y_range, zs = z_min_const, color = "blue")
        plt.plot(x_min_const, y_range, zs = z_max_const, color = "blue")
        plt.plot(x_max_const, y_range, zs = z_min_const, color = "blue")
        plt.plot(x_max_const, y_range, zs = z_max_const, color = "blue")

        plt.plot(x_range, y_min_const, zs = z_min_const, color = "blue")
        plt.plot(x_range, y_min_const, zs = z_max_const, color = "blue")
        plt.plot(x_range, y_max_const, zs = z_min_const, color = "blue")
        plt.plot(x_range, y_max_const, zs = z_max_const, color = "blue")

    plt.plot(x_coords, y_coords, zs = z_coords, color = "red")
    plt.show() 
    plt.close()     
    '''
 
    boxes_matrix = [[[0 for z in range(max_box_z - min_box_z + 1)] for y in range(max_box_y - min_box_y + 1)] for x in range(max_box_x - min_box_x + 1)]
    for box in used_boxes:
        x, y, z = box 
        boxes_matrix[x - min_box_x][y - min_box_y][z - min_box_z] = 1
    boxes_matrix = np.array(boxes_matrix)

    return boxes_matrix 

len_traj = 600
actual_step_size = 10 ** -2
x_offsets = np.random.rand(len_traj) * 2 * actual_step_size - actual_step_size
y_offsets = np.random.rand(len_traj) * 2 * actual_step_size - actual_step_size
z_offsets = np.random.rand(len_traj) * 2 * actual_step_size - actual_step_size
 
  
x_coord = [sum(x_offsets[:i]) for i in range(len_traj)]
y_coord = [sum(y_offsets[:i]) for i in range(len_traj)]
z_coord = [sum(z_offsets[:i]) for i in range(len_traj)]
  
sorted_x = sorted(x_coord)
sorted_y = sorted(y_coord)
sorted_z = sorted(z_coord)
 
fig = plt.figure()
ax = plt.axes(projection='3d') 
plt.plot(x_coord, y_coord, zs = z_coord, color = "red")
plt.show() 
plt.close()   

nparr = get_boxes(x_coord, y_coord, z_coord) 
fd = fractal_dimension(nparr)
print(fd)

fig = plt.figure()
ax = plt.axes(projection='3d') 
plt.plot(sorted_x, sorted_y, zs = sorted_z, color = "red")
plt.show() 
plt.close()   

snparr = get_boxes(sorted_x, sorted_y, sorted_z) 
sfd = fractal_dimension(snparr)
print(sfd)

print(len(os.listdir("usable_trajs")))
cnt = 0
fig = plt.figure()
#ax = plt.axes(projection='3d') 
for usable_traj_filename in os.listdir("usable_trajs"):

    pd_file = pd.read_csv("usable_trajs/" + usable_traj_filename, index_col = False)
    old_len = len(pd_file)
    pd_file = pd_file.dropna(subset = ["lon", "lat", "baroaltitude"]) 
    if len(pd_file) != old_len:
        continue

    if not "lat" in pd_file.columns:
        continue
    else:
        cnt += 1 
    
    if cnt == 1000:
        break
      
    x_c = list(pd_file["lon"])
    y_c = list(pd_file["lat"]) 
    z_c = [z / 1000 for z in pd_file["baroaltitude"]]
    z_const = [1 for z in pd_file["baroaltitude"]]
 
    utm_vals = []
    easting_val = []
    northing_val = []

    for j in range(len(x_c)):
        utm_val = utm.from_latlon(y_c[j], x_c[j])
        utm_vals.append(utm_val)
        easting_val.append(utm_val[0] / 1000)
        northing_val.append(utm_val[1] / 1000)

    print(usable_traj_filename)  
 
    #plt.plot(easting_val, northing_val, zs = z_c)
    plt.plot(easting_val[:20], northing_val[:20])
    '''
    plt.show() 
    plt.close()    

    barr = get_boxes(easting_val, northing_val, z_c) 
    tfd = fractal_dimension(barr)
    print(tfd)
    
    fig = plt.figure()
    ax = plt.axes(projection='3d') 
    plt.plot(easting_val, northing_val, zs = z_const, color = "red")
    plt.show() 
    plt.close()   

    barr_const = get_boxes(easting_val, northing_val, z_const) 
    tfd_const = fractal_dimension(barr_const)
    print(tfd_const)
    ''' 
  
plt.show() 
plt.close()   

print(cnt)