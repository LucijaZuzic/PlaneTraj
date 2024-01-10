import numpy as np
import matplotlib.pyplot as plt
from utilities import random_colors

lens = 1000
mini_dim = 1
maxi_dim = 10

x_coords = sorted(np.random.rand(lens))
y_coords = sorted(np.random.rand(lens))
z_coords = sorted(np.random.rand(lens))
z_coords = [1 for x in x_coords]

x_min = min(x_coords)
x_max = max(x_coords)

y_min = min(y_coords)
y_max = max(y_coords)

z_min = min(z_coords)
z_max = max(z_coords)

total_min = min(min(x_min, y_min), z_min)
total_max = max(max(x_max, y_max), z_max)

box_sizes = [10 ** (- 1) * x for x in range(mini_dim, maxi_dim + 1)]

for box_size in box_sizes:

    box_starts = np.arange(total_min, total_max + box_size, box_size)

    #rcs = random_colors((len(box_starts) - 1) ** 3)
    print(box_size)

    dict_boxes = dict()
    used_boxes = set()
    used_x = set()
    used_y = set()
    used_z = set()

    for p in range(lens):

        px_curr = x_coords[p]
        py_curr = y_coords[p]
        pz_curr = z_coords[p]
 
        if p != lens - 1: 
            px_next = x_coords[p + 1]
            py_next = y_coords[p + 1]
            pz_next = z_coords[p + 1]
        else:
            px_next = x_coords[p]
            py_next = y_coords[p]
            pz_next = z_coords[p]

        x_start = max(px_curr, px_next)
        y_start = max(py_curr, py_next)
        z_start = max(pz_curr, pz_next)

        x_end = min(px_curr, px_next)
        y_end = min(py_curr, py_next)
        z_end = min(pz_curr, pz_next)

        for px in np.arange(x_start, x_end + box_size, box_size):
            for py in np.arange(y_start, y_end + box_size, box_size):
                for pz in np.arange(z_start, z_end + box_size, box_size): 

                    x_box = int(px // box_size)
                    y_box = int(py // box_size)
                    z_box = int(pz // box_size)

                    if (x_box, y_box, z_box) not in dict_boxes:
                        dict_boxes[(x_box, y_box, z_box)] = []
                    else:
                        dict_boxes[(x_box, y_box, z_box)].append((px, py, pz))

                    used_boxes.add((x_box, y_box, z_box))
                    used_x.add(x_box)
                    used_y.add(y_box)
                    used_z.add(z_box)

    #for bx in dict_boxes:
        #print(bx, len(dict_boxes[bx]))

    print(len(dict_boxes))
    print(len(used_x))
    print(len(used_y))
    print(len(used_z))

    if len(dict_boxes) < 10:
        for bx in dict_boxes:
            print(bx, len(dict_boxes[bx]))

    fig = plt.figure()
    ax = plt.axes(projection='3d')
   
    '''
    rising = [bs for bs in box_starts]
    for v1 in box_starts:
        const_v1 = [v1 for bs in box_starts]
        for v2 in box_starts:
            const_v2 = [v2 for bs in box_starts]
            plt.plot(const_v1, const_v2, zs = rising, color = "blue")
            plt.plot(const_v1, rising, zs = const_v2, color = "green")
            plt.plot(rising, const_v1, zs = const_v2, color = "yellow")
    '''
  
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