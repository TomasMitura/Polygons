from tkinter import Y
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

def draw_contours(edges, depth_file, y_start, y_increment, y_max, base_depth, end_depth, speed_off, speed_on, fab_file):
    # Load data from Excel file
    df = pd.read_excel(depth_file)

    # Extract energy and depth columns from the DataFrame
    energy_data = df["Voltage"].values
    depth_data = df["Depth"].values

    # Create an interpolation function
    interp_func = interp1d(depth_data, energy_data, kind='linear', fill_value=(energy_data[0], energy_data[-1]))    

    intersection_points = []  # To store intersection points
    
    depth = base_depth
    y_coord = y_start
    z = 0

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
        laser_output = interp_func(depth)
        fab_file.write(f"c\t0\t{x1:.6f}\t{y1:.6f}\t{z:.6f}\t{speed_off:.6f}\t{speed_off:.6f}\t{speed_off:.6f}\t0.000000\t0\n")
        fab_file.write(f"c\t1\t{x2:.6f}\t{y2:.6f}\t{z:.6f}\t{speed_on:.6f}\t{speed_on:.6f}\t{speed_on:.6f}\t{laser_output:.6f}\t0\n")

# Laser settings
if __name__ == "__main__":
    with open(r'C:\Users\mitura\source\repos\Polygons\Polygons\3D_parameter_input.yaml') as file:
        input_dict = yaml.load(file, Loader=yaml.FullLoader)
        speed_off = input_dict['speed_off']
        speed_on = input_dict['speed_on']
        base_depth = input_dict['base_depth']
        end_depth = input_dict['end_depth']
        y_start = input_dict['y_start']
        y_increment = input_dict['y_increment']
        y_max = input_dict['y_max']        
        depth_file = input_dict['calibration_file']
        output_file = input_dict['output_file']
        polygon_3D = input_dict['3D_polygon']
        print(input_dict)
        
    
        
    # Extract x, y, and z coordinates from the loaded 3D data
    vertices_3d = [(point['x'], point['y'], point['z']) for point in polygon_3D]

    # Convert the list of tuples to a NumPy array for further processing if needed
    vertices_3d_array = np.array(vertices_3d, dtype=float)

    # Project 3D coordinates to 2D (top-down view)
    edges = [(x, y) for x, y, z in vertices_3d]

    # Create edges by connecting the points
    edges = list(zip(edges, edges[1:] + edges[:1]))

    # Convert edges to NumPy arrays
    edges = [np.array(edge, dtype=float) for edge in edges]

    # Shift all edge coordinates to positive values by adding the absolute minimum value for each dimension
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

    max_coord = max(max_x - min_x, max_y - min_y)

    if max_coord > 1:
        for edge in edges:
            edge /= max_coord

with open(output_file, "w") as fab_file:
    draw_contours(edges, depth_file, y_start, y_increment, y_max, base_depth, end_depth, speed_off, speed_on, fab_file)

plt.figure()

# Draw the polygon outline
draw_polygon(edges)
#draw_polygon(edges_2)

# Show the plot
plt.axis('equal')  # Set aspect ratio to equal for a consistent scale
plt.show()

