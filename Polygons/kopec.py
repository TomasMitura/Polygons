import matplotlib.pyplot as plt
import sys
import numpy as np
from scipy.interpolate import interp1d
import pandas as pd

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

def draw_contours(edges, depth_file, base_depth, end_depth, fab_file):
    # Load data from Excel file
    df = pd.read_excel(depth_file)

    # Extract energy and depth columns from the DataFrame
    energy_data = df["Voltage"].values
    depth_data = df["Depth"].values

    # Create an interpolation function
    interp_func = interp1d(depth_data, energy_data, kind='linear', fill_value=(energy_data[0], energy_data[-1]))    

    intersection_points = []  # To store intersection points
    
    y_coord = 0.0
    y_increment = 0.001
    y_max = 1.0
    
    depth = base_depth
    depth_increment = (base_depth - end_depth)/(0.5*(y_max/y_increment))

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
    
    previous_y = intersection_points[1][1]

    for i in range(0, len(intersection_points)-1, 2):
        x1, y1 = intersection_points[i]
        x2, y2 = intersection_points[i + 1]
        if y1 > previous_y:
            if depth <= end_depth:
                depth_increment = -depth_increment
            depth += depth_increment
        laser_output = interp_func(depth)
        fab_file.write(f"c\t0\t{x1:.6f}\t{y1:.6f}\t0.000000\t{speed_off:.6f}\t{speed_off:.6f}\t{speed_off:.6f}\t0.000000\t0\n")
        fab_file.write(f"c\t1\t{x2:.6f}\t{y2:.6f}\t0.000000\t{speed_on:.6f}\t{speed_on:.6f}\t{speed_on:.6f}\t{laser_output:.6f}\t0\n")
        previous_y = y1


polygon =[(-40,0),(-21,11),(-1,0),(-4,14),(34,0),(40,12),(49,12),(49,23),(48,29),(28,7),(15,28),(12,12),(-13,27),(-21,18),(-30,26),(-38,26),(-28,14)]


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
    
print(edges)

# Laser settings
if __name__ == "__main__":
    speed_off = float(sys.argv[1])
    speed_on = float(sys.argv[2])
    base_depth = 100.0
    end_depth = 70.0

depth_file = r"C:\Users\mitura\Documents\Python_scripts\Depth\Vd_Interpolated060923.xlsx"
output_file = r"C:\Users\mitura\Documents\Python_scripts\Polygon\Polygon_draw_Test_kopec.fab"
with open(output_file, "w") as fab_file:
    draw_contours(edges, depth_file, base_depth, end_depth, fab_file) #add + edges_2 if you want second shape

plt.figure()

# Draw the polygon outline
draw_polygon(edges)
#draw_polygon(edges_2)

# Show the plot
plt.axis('equal')  # Set aspect ratio to equal for a consistent scale
plt.show()