import numpy as np
import matplotlib.pyplot as plt 
 
#mini_dim = 10 ** -1
#maxi_dim = 1
#step_size = 10 ** -1

def get_fractal_dim_for_coords(x_coords, y_coords, z_coords):

    x_min = min(x_coords)
    x_max = max(x_coords)

    y_min = min(y_coords)
    y_max = max(y_coords)

    z_min = min(z_coords)
    z_max = max(z_coords)

    #total_min = min(min(x_min, y_min), z_min)
    #total_max = max(max(x_max, y_max), z_max)

    used_boxes_for_box_sizes = []

    num_boxes_for_box_sizes = []

    total_len_for_box_sizes = []

    fractal_dimension_vals = []

    #box_sizes = [x for x in np.arange(mini_dim, maxi_dim + step_size, step_size)]

    box_sizes = []
    for expon in range(2, 0, -1):
        box_sizes_tmp = [10 ** (- expon) * x for x in range(1, 2, 1)]
        for tmp_val in box_sizes_tmp:
            box_sizes.append(tmp_val) 
    box_sizes.append(1) 

    for box_size in box_sizes: 

        #box_starts = np.arange(total_min, total_max + box_size, box_size)
        #print(box_size, len(box_starts))
    
        #used_boxes = set() 

        num_boxes = 0

        for p in range(len(x_coords) - 1):

            px = x_coords[p]
            py = y_coords[p]
            pz = z_coords[p] 

            x_box = int(px // box_size)
            y_box = int(py // box_size)
            z_box = int(pz // box_size)
       
            px_next = x_coords[p + 1]
            py_next = y_coords[p + 1]
            pz_next = z_coords[p + 1] 

            x_box_next = int(px_next // box_size)
            y_box_next = int(py_next // box_size)
            z_box_next = int(pz_next // box_size)

            min_box_x = min(x_box, x_box_next)
            max_box_x = max(x_box, x_box_next)
            min_box_y = min(y_box, y_box_next)
            max_box_y = max(y_box, y_box_next)
            min_box_z = min(z_box, z_box_next)
            max_box_z = max(z_box, z_box_next)
            
            num_boxes += (max_box_x - min_box_x + 1) * (max_box_y - min_box_y + 1) *(max_box_z - min_box_z + 1)
             
            #for x_box_curr in range(min_box_x, max_box_x + 1):
                #for y_box_curr in range(min_box_y, max_box_y + 1):
                    #for z_box_curr in range(min_box_z, max_box_z + 1):

                        #used_boxes.add((x_box_curr, y_box_curr, z_box_curr))
        
        #used_boxes_for_box_sizes.append(len(used_boxes))
        #print(len(used_boxes), box_size)  
        num_boxes_for_box_sizes.append(num_boxes) 
        total_len_for_box_sizes.append(num_boxes * box_size * np.sqrt(3))
        print(num_boxes, num_boxes * box_size * np.sqrt(3), box_size) 
        fractal_dimension_vals.append(np.log(num_boxes) / np.log(box_size ** -1))
        
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

    plt.plot([i for i in range(len(total_len_for_box_sizes))], total_len_for_box_sizes)
    plt.show()
    plt.close()

    plt.plot([i for i in range(len(num_boxes_for_box_sizes))], num_boxes_for_box_sizes)
    plt.show()
    plt.close()

    #plt.plot([i for i in range(len(used_boxes_for_box_sizes))], used_boxes_for_box_sizes)
    #plt.show()
    #plt.close()

    #plt.plot(box_sizes, fractal_dimension_vals)
    #plt.show()
    #plt.close()

    #return fractal_dimension_vals[0]

len_traj = 1000
actual_step_size = 1
x_offsets = np.random.rand(len_traj) * 2 * actual_step_size - actual_step_size
y_offsets = np.random.rand(len_traj) * 2 * actual_step_size - actual_step_size
z_offsets = np.random.rand(len_traj) * 2 * actual_step_size - actual_step_size
  
x_coord = [sum(x_offsets[:i]) for i in range(len_traj)]
y_coord = [sum(y_offsets[:i]) for i in range(len_traj)]
z_coord = [sum(z_offsets[:i]) for i in range(len_traj)]

total_off = 0
for i in range(1, len_traj):
    x_off = x_coord[i] - x_coord[i - 1]
    y_off = y_coord[i] - y_coord[i - 1]
    z_off = z_coord[i] - z_coord[i - 1]
    xy_off = np.sqrt(x_off ** 2 + y_off ** 2)
    total_off += np.sqrt(z_off ** 2 + xy_off ** 2) 
print(total_off)

fig = plt.figure()
ax = plt.axes(projection='3d')
plt.plot(x_coord, y_coord, zs = z_coord)
plt.show()
plt.close()

get_fractal_dim_for_coords(x_coord, y_coord, z_coord)