import matplotlib.pyplot as plt
import sys
import numpy as np
from scipy.interpolate import interp1d
import pandas as pd
import yaml

def draw_point(pt):
    x, y = pt
    plt.plot(x, y, "go", markersize=5)

def draw_polygon(edges):
    for edge in edges:
        x_coords, y_coords = zip(*edge)
        plt.plot(x_coords, y_coords, "b-")

def generate_intersection(line_a, line_b):
    pt1, pt2 = line_a
    pt3, pt4 = line_b
    x1, y1 = pt1
    x2, y2 = pt2
    x3, y3 = pt3
    x4, y4 = pt4

    divisor = ((x1 - x2)*(y3 - y4) - (y1 - y2)*(x3 - x4))
    if divisor == 0:
        return None

    t = ((x1 - x3)*(y3 - y4) - (y1 - y3)*(x3 - x4)) / divisor
    if 0 <= t and t <= 1:
        return round(x1 + t*(x2 - x1), 6), round(y1 + t*(y2 - y1), 6)
    return None

def draw_contours(edges, calibration_file, y_coord, y_increment, y_max, base_depth, speed_off, speed_on, fab_file):
    # Load data from Excel file
    df = pd.read_excel(calibration_file)

    # Extract energy and depth columns from the DataFrame
    energy_data = df["Voltage"].values
    depth_data = df["Depth"].values

    # Create an interpolation function
    interp_func = interp1d(depth_data, energy_data, kind='linear', fill_value=(energy_data[0], energy_data[-1]))    

    intersection_points = []  # To store intersection points

    depth = base_depth

    while y_coord <= y_max:
        horizontal_line = ((0, y_coord), (1, y_coord))
        for edge in edges:
            intersection = generate_intersection(edge, horizontal_line)
            if intersection is not None:
                draw_point(intersection)
                intersection_points.append(intersection)
            if edge[0][1] == edge[1][1] == y_coord:
                intersection_points.extend([((edge[0][0]), (edge[0][1])),
                                            ((edge[1][0]), (edge[1][1]))])
        y_coord += y_increment
    # Sort intersection points based on y-coordinates
    intersection_points.sort(key=lambda point: point[0])
    intersection_points.sort(key=lambda point: point[1])
    
    fab_file.write(f"p\t1\n")

    for i in range(0, len(intersection_points)-1, 2):
        x1, y1 = intersection_points[i]
        x2, y2 = intersection_points[i + 1]
        if y1 < 0.40384:
            depth = 95
        elif (y1 > 0.5) and (y1 < 0.6153) :
            depth = 85
        elif  (y1 > 0.7115) and (y1 < 0.8076):
            depth = 75
        elif y1 > 0.9038:  
            depth = 65
        else:
            depth = 100    
        laser_output = interp_func(depth)
        fab_file.write(f"c\t0\t{x1:.6f}\t{y1:.6f}\t0.000000\t{speed_off:.6f}\t{speed_off:.6f}\t{speed_off:.6f}\t0.000000\t0\n")
        fab_file.write(f"c\t1\t{x2:.6f}\t{y2:.6f}\t0.000000\t{speed_on:.6f}\t{speed_on:.6f}\t{speed_on:.6f}\t{laser_output:.6f}\t0\n")


#polygon =[(-40,0),(-21,11),(-1,0),(-4,14),(34,0),(40,12),(49,12),(49,23),(48,29),(28,7),(15,28),(12,12),(-13,27),(-21,18),(-30,26),(-38,26),(-28,14)]

polygon = [
    (0.43, 0.5),
    (0.684, 0.5),
    (0.684, 0.404),
    (0.43, 0.404),
    (0.43, 0.308),
    (1.0, 0.308),
    (1.0, 0.404),
    (0.747, 0.404),
    (0.747, 0.5),
    (1.0, 0.5),
    (1.0, 0.615),
    (0.747, 0.615),
    (0.747, 0.712),
    (1.0, 0.712),
    (1.0, 0.808),
    (0.747, 0.808),
    (0.747, 0.904),
    (1.0, 0.904),
    (1.0, 1.0),
    (0.43, 1.0),
    (0.43, 0.904),
    (0.684, 0.904),
    (0.684, 0.808),
    (0.43, 0.808),
    (0.43, 0.712),
    (0.684, 0.712),
    (0.684, 0.615),
    (0.43, 0.615)
]



edges = list(zip(polygon, polygon[1:] + polygon[:1]))
#edges_2 = list(zip(polygon_2, polygon_2[1:] + polygon_2[:1]))

edges = [np.array(edge, dtype=float) for edge in edges]

# Shift all edge coordinates to positive values by adding the absolute minimum value
min_x = min(np.min(edge[:, 0]) for edge in edges)
min_y = min(np.min(edge[:, 1]) for edge in edges)

if min_x < 0:
    for edge in edges:
        edge[:, 0] += abs(min_x)
if min_y < 0:
    for edge in edges:
        edge[:, 1] += abs(min_y)

# Normalize the coordinates of edges to the range [0, 1]
max_x = max(np.max(edge[:, 0]) for edge in edges)
max_y = max(np.max(edge[:, 1]) for edge in edges)

if max_x > 1 or max_y > 1:
    for edge in edges:
        edge /= np.array([max_x, max_y])

# Laser settings
if __name__ == "__main__":
    with open(r'C:\Users\mitura\source\repos\Polygons\Polygons\parameter_input.yaml') as file:
        input_dict = yaml.load(file, Loader=yaml.FullLoader)
        speed_off = input_dict['speed_off']
        speed_on = input_dict['speed_on']
        base_depth = input_dict['base_depth']
        end_depth = input_dict['end_depth']
        y_coord = input_dict['y_coord']
        y_increment = input_dict['y_increment']
        y_max = input_dict['y_max']  
        calibration_file = input_dict['calibration_file']
        output_file = input_dict['output_file']

        print(input_dict)
        
    #create a text version of the inputs
    text_content = "\n".join([f"{key}: {value}" for key, value in input_dict.items()])
    
    #store the inputs in a text file for future reference
    with open(r"C:\Users\mitura\Documents\Python_scripts\Polygon\Polygon_inputs.txt", 'w') as text_file:
        text_file.write(text_content)

with open(output_file, "w") as fab_file:
    draw_contours(edges, calibration_file, y_coord, y_increment, y_max, base_depth, speed_off, speed_on, fab_file) #add + edges_2 if you want second shape

plt.figure()

# Draw the polygon outline
draw_polygon(edges)
#draw_polygon(edges_2)

# Show the plot
plt.axis('equal')  # Set aspect ratio to equal for a consistent scale
plt.show()