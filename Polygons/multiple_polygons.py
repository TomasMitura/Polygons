from tkinter import Y
import matplotlib.pyplot as plt
import sys
import numpy as np
from scipy.interpolate import interp1d
import pandas as pd
import yaml

def generate_intersection(line_a, line_b):
    ((x1, y1), (x2, y2)) = line_a
    ((x3, y3), (x4, y4)) = line_b

    divisor = ((x1 - x2)*(y3 - y4) - (y1 - y2)*(x3 - x4))
    if divisor == 0:
        return None

    t = ((x1 - x3)*(y3 - y4) - (y1 - y3)*(x3 - x4)) / divisor
    if 0 <= t and t <= 1:
        return round(x1 + t*(x2 - x1), 6), round(y1 + t*(y2 - y1), 6)
    return None

def draw_contours(edges, depth_file, x_min, x_max, y_min, y_increment, y_max, base_depth, end_depth, slow_speed, speed_off, base_speed, fab_file):
    # Load data from Excel file
    df = pd.read_excel(depth_file)

    # Extract energy and depth columns from the DataFrame
    energy_data = df["Voltage"].values
    depth_data = df["Depth"].values

    # Create an interpolation function
    interp_func = interp1d(depth_data, energy_data, kind='linear', fill_value=(energy_data[0], energy_data[-1]))    

    intersection_points = []  # To store intersection points
    

    for key, edge_array in edges.items():
        depth = base_depth
        speed_on = base_speed
        y_coord = y_min

        while y_coord <= y_max:
            horizontal_line = ((x_min, y_coord), (x_max, y_coord))
            for edge in edge_array:
                intersection = generate_intersection(edge, horizontal_line)
                if intersection is not None:
                    intersection_points.append(intersection)
                if edge[0][1] == edge[1][1] == y_coord:
                    intersection_points.extend([((edge[0][0]), (edge[0][1])),
                                                ((edge[1][0]), (edge[1][1]))])
            y_coord += y_increment
    # Sort intersection points based on y-coordinates
    intersection_points.sort(key=lambda point: point[0])
    intersection_points.sort(key=lambda point: point[1])
    
    previous_y = intersection_points[1][1]

    fab_file.write(f"p\t1\n")
    
    for i in range(0, len(intersection_points)-1, 2):
        x1, y1 = intersection_points[i]
        x2, y2 = intersection_points[i + 1]
        laser_output = interp_func(depth)
        if abs(x1-x2)<0.001:
            pass
        else:    
            if (x2 - x1) < 0.09:
                speed_on = slow_speed
                laser_output = ((laser_output - 0.5)/(base_speed/slow_speed))+0.5
            else:
                speed_on = base_speed
            fab_file.write(f"c\t0\t{x1:.6f}\t{y1:.6f}\t0.000000\t{speed_off:.6f}\t{speed_off:.6f}\t{speed_off:.6f}\t0.000000\t0\n")
            fab_file.write(f"c\t1\t{x2:.6f}\t{y2:.6f}\t0.000000\t{speed_on:.6f}\t{speed_on:.6f}\t{speed_on:.6f}\t{laser_output:.6f}\t0\n")
            previous_y = y1

# Laser settings
if __name__ == "__main__":
    with open(r'C:\Users\mitura\source\repos\Polygons\Polygons\parameter_input.yaml') as file:
        input_dict = yaml.load(file, Loader=yaml.FullLoader)
        speed_off = input_dict['speed_off']
        base_speed = input_dict['base_speed']
        base_depth = input_dict['base_depth']
        end_depth = input_dict['end_depth']
        y_increment = input_dict['y_increment']       
        slow_speed = input_dict['slow_speed']
        depth_file = input_dict['calibration_file']
        output_file = input_dict['output_file']
        polygon_arrays = {}

        for key in input_dict:
            if key.startswith('polygon_'):
                polygon_arrays[key] = [(x, y) for x, y in input_dict[key]]
                
        #Initialize largest x and y with negative infinity
        largest_x = float('-inf')
        largest_y = float('-inf')

        #Iterate through the input_dict to find the smallest x and y values
        for key in input_dict:
            if key.startswith('polygon_'):
                 coordinates = input_dict[key]
                 for coord in coordinates:
                     x, y = float(coord['x']), float(coord['y'])
                     smallest_x = min(smallest_x, x)
                     smallest_y = min(smallest_y, y)

        #Print the smallest x and y after normalization
        print("Largest x:", largest_x)
        print("Largest y:", largest_y)
        print("Smallest x:", smallest_x)
        print("Smallest y:", smallest_y)

        #Store the min and max values for x and y
        x_min = smallest_x
        x_max = largest_x 
        y_min = smallest_y
        y_max = largest_y
            

        edges = {}

        # Iterate through polygon_arrays
        for key, value in input_dict.items():
            if key.startswith('polygon_'):
                # Extract the polygon number from the key
                polygon_number = int(key.split('_')[1])
                # Assuming value is a list of dictionaries with 'x' and 'y' keys
                polygon_coordinates = [(point['x'], point['y']) for point in value]
                # Store the coordinates in the polygon_arrays dictionary
                polygon_arrays[f'polygon_{polygon_number}'] = polygon_coordinates
                # Create edges for the polygon
                num_points = len(polygon_coordinates)
                edges_key = f'edges_{polygon_number}'
                edges[edges_key] = tuple(((polygon_coordinates[i], polygon_coordinates[(i + 1) % num_points]) for i in range(num_points)))

with open(output_file, "w") as fab_file:
    draw_contours(edges, depth_file, x_min, x_max, y_min, y_increment, y_max, base_depth, end_depth, slow_speed, speed_off, base_speed, fab_file)
    

# Normalize the coordinates to range from 0 to 1
# for key in input_dict:
#     if key.startswith('polygon_'):
#         coordinates = input_dict[key]
#         for coord in coordinates:
#             coord['x'] = (float(coord['x']) / largest_x)
#             coord['y'] = (float(coord['y']) / largest_y)



