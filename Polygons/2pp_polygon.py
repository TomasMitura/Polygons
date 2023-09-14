import matplotlib.pyplot as plt
import numpy as np
import yaml

def draw_point(pt):
    x, y = pt
    plt.plot(x, y, "go", markersize=5)

def draw_polygon(edges):
    for edge in edges:
        x_coords, y_coords = zip(*edge)
        plt.plot(x_coords, y_coords, "b-")

def draw_contours(fab_file, base_z, z_max, z_increment, speed_on, laser_output):
    fab_file.write(f"p\t1\n")
        
    z = base_z
    x, y = polygon[0]
    fab_file.write(f"c\t0\t{x:.6f}\t{y:.6f}\t{z:.6f}\t{speed_on:.6f}\t{speed_on:.6f}\t{speed_on:.6f}\t0.000000\t0\n")
    
    while z <= z_max:
        for i, (x, y) in enumerate(polygon):         
            fab_file.write(f"c\t0\t{x:.6f}\t{y:.6f}\t{z:.6f}\t{speed_on:.6f}\t{speed_on:.6f}\t{speed_on:.6f}\t{laser_output:.6f}\t0\n")
        z += z_increment
        fab_file.write(f"c\t0\t{x:.6f}\t{y:.6f}\t{z:.6f}\t{speed_on:.6f}\t{speed_on:.6f}\t{speed_on:.6f}\t0.000000\t0\n")
# Laser settings
if __name__ == "__main__":
    with open(r'C:\Users\mitura\source\repos\Polygons\Polygons\2pp_parameter_input.yaml') as file:
        input_dict = yaml.load(file, Loader=yaml.FullLoader)
        laser_output = input_dict['laser_output']
        speed_on = input_dict['speed_on']
        base_z = input_dict['base_z'] 
        z_max = input_dict['z_max']
        z_increment = input_dict['z_increment']
        output_file = input_dict['output_file']
        polygon = input_dict['polygon']
        print(input_dict)
        
    
    polygon = [(point['x'], point['y']) for point in polygon]
        
    edges = list(zip(polygon, polygon[1:] + polygon[:1]))

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
    if max_y > max_x:
        max_coord = max_y
    else:
        max_coord = max_x
    if max_coord > 1:
        for edge in edges:
            edge /= np.array([max_coord, max_coord])

with open(output_file, "w") as fab_file:
    draw_contours(fab_file, base_z, z_max, z_increment, speed_on, laser_output)

plt.figure()

# Draw the polygon outline
draw_polygon(edges)
#draw_polygon(edges_2)

# Show the plot
plt.axis('equal')  # Set aspect ratio to equal for a consistent scale
plt.show()

