import matplotlib.pyplot as plt
import yaml
import math

def draw_contours(fab_file, x_coords, y_coords, z_coords, speed_on, laser_output):
    fab_file.write("p\t2\n")
    sorted_coords = sorted(zip(x_coords, y_coords, z_coords), key=lambda coord: (coord[1], coord[2], coord[0]))
    
    for x, y, z in sorted_coords:
        fab_file.write(f"c\t0\t{x:.6f}\t{y:.6f}\t{z:.6f}\t{speed_on:.6f}\t{speed_on:.6f}\t{speed_on:.6f}\t{laser_output:.6f}\t0\n")


# Laser settings
if __name__ == "__main__":
    with open(r'C:\Users\mitura\source\repos\Polygons\Polygons\3D_2pp_input.yaml') as file:
        input_dict = yaml.load(file, Loader=yaml.FullLoader)
        laser_output = input_dict['laser_output']
        speed_on = input_dict['speed_on']
        output_file = input_dict['output_file']
        
    with open(r'C:\Users\mitura\Documents\Python_scripts\Objects\Slopes.yaml') as file:
        polygon_data = yaml.load(file, Loader=yaml.FullLoader)
        polygon = polygon_data.get('points', [])
    
    x_coords = [point['x'] for point in polygon]
    y_coords = [point['y'] for point in polygon]
    z_coords = [point['z'] for point in polygon]
    
    print("Polygon points:", polygon)


with open(output_file, "w") as fab_file:
    draw_contours(fab_file, x_coords, y_coords, z_coords, speed_on, laser_output)

# Plot the perimeter of the polygon
plt.plot(x_coords, y_coords, 'b-')

# Set labels and title
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Polygon Perimeter')

# Show the plot
plt.axis('equal')  # Set aspect ratio to equal for a consistent scale
plt.show()