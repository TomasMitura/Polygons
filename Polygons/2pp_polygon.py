import matplotlib.pyplot as plt
import yaml
import math

def draw_contours(fab_file, x_coords, y_coords, base_z, z_max, z_increment, speed_on, laser_output):
    fab_file.write("p\t2\n")
        
    z = base_z
    x, y = x_coords[0], y_coords[0]
    fab_file.write(f"c\t0\t{x:.6f}\t{y:.6f}\t{z:.6f}\t{speed_on:.6f}\t{speed_on:.6f}\t{speed_on:.6f}\t0.000000\t0\n")
    
    while z <= z_max:
        for i in range(len(x_coords)):
            x, y = x_coords[i], y_coords[i]
            fab_file.write(f"c\t0\t{x:.6f}\t{y:.6f}\t{z:.6f}\t{speed_on:.6f}\t{speed_on:.6f}\t{speed_on:.6f}\t{laser_output:.6f}\t0\n")
        z += z_increment


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
        print("Polygon points:", polygon)
        
    
    x_coords = [point['x'] for point in polygon]
    y_coords = [point['y'] for point in polygon]
    
    print("Polygon points:", polygon)


with open(output_file, "w") as fab_file:
    draw_contours(fab_file, x_coords, y_coords, base_z, z_max, z_increment, speed_on, laser_output)

# Plot the perimeter of the polygon
plt.plot(x_coords, y_coords, 'b-')

# Set labels and title
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Polygon Perimeter')

# Show the plot
plt.axis('equal')  # Set aspect ratio to equal for a consistent scale
plt.show()