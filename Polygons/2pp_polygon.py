import matplotlib.pyplot as plt
import numpy as np
import yaml

def draw_point(pt):
    x, y = pt
    plt.plot(x, y, "go", markersize=5)

def draw_polygon(polygon):
    for poly in polygon:
        x_coords, y_coords = zip(*poly)
        plt.plot(x_coords, y_coords, "b-")

def draw_contours(fab_file, base_z, z_max, z_increment, speed_on, laser_output):
    fab_file.write(f"p\t2\n")
        
    z = base_z
    x, y = polygon[0][0]
    fab_file.write(f"c\t0\t{x:.6f}\t{y:.6f}\t{z:.6f}\t{speed_on:.6f}\t{speed_on:.6f}\t{speed_on:.6f}\t0.000000\t0\n")
    
    while z <= z_max:
        for i in range(len(polygon)):
            x, y = polygon[i]
            fab_file.write(f"c\t0\t{x[0]:.6f}\t{y[0]:.6f}\t{z:.6f}\t{speed_on:.6f}\t{speed_on:.6f}\t{speed_on:.6f}\t{laser_output:.6f}\t0\n")
        z += z_increment
        fab_file.write(f"c\t0\t{x[0]:.6f}\t{y[0]:.6f}\t{z:.6f}\t{speed_on:.6f}\t{speed_on:.6f}\t{speed_on:.6f}\t0.000000\t0\n")

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
        
    polygon = list(zip(polygon, polygon[1:] + polygon[:1]))

    polygon = [np.array(poly, dtype=float) for poly in polygon]

    # Shift all poly coordinates to positive values by adding the absolute minimum value
    min_x = min(np.min(poly[:, 0]) for poly in polygon)
    min_y = min(np.min(poly[:, 1]) for poly in polygon)

    if min_x < 0:
        for poly in polygon:
            poly[:, 0] += abs(min_x)
    if min_y < 0:
        for poly in polygon:
            poly[:, 1] += abs(min_y)

    # Normalize the coordinates of polygon to the range [0, 1]
    max_x = max(np.max(poly[:, 0]) for poly in polygon)
    max_y = max(np.max(poly[:, 1]) for poly in polygon)
    if max_y > max_x:
        max_coord = max_y
    else:
        max_coord = max_x
    if max_coord > 1:
        for poly in polygon:
            poly /= np.array([max_coord, max_coord])

with open(output_file, "w") as fab_file:
    draw_contours(fab_file, base_z, z_max, z_increment, speed_on, laser_output)

plt.figure()

# Draw the polygon outline
draw_polygon(polygon)
#draw_polygon(polygon_2)

# Show the plot
plt.axis('equal')  # Set aspect ratio to equal for a consistent scale
plt.show()

