import matplotlib.pyplot as plt
import yaml
import math
from mpl_toolkits.mplot3d import Axes3D

def visualize_3d_points(x_coords, y_coords, z_coords):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    # Plot the points
    ax.scatter(x_coords, y_coords, z_coords, c='b', marker='o')

    # Connect the points with lines
    for i in range(len(x_coords) - 1):
        ax.plot([x_coords[i], x_coords[i + 1]], [y_coords[i], y_coords[i + 1]], [z_coords[i], z_coords[i + 1]], c='r')

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    plt.show()

def draw_contours(fab_file, x_repetition, y_repetition, build_polygon, z_height, z_step, x_coords, y_coords, z_coords, speed_on, laser_output, max_x, max_y, max_z, min_x, min_y, min_z, spacing, crosses, cross_spacing, overhang_x, overhang_y):
    fab_file.write("p\t2\n")
    x_move = 0
    y_move = 0
    n = 1
    m = 1
    speed_return = 80.0
    speed_save_point = speed_on
    laser_output_save_point = laser_output       
    #Array repetition if we have more than 1 repetition
    if y_repetition or x_repetition > 1:
        for n in range(y_repetition):
            modified_y_coords = [y + n * y_move for y in y_coords]
            for m in range(x_repetition):
                modified_x_coords = [x + m * x_move for x in x_coords]
                for i in range(len(x_coords)):
                    x, y, z = modified_x_coords[i], modified_y_coords[i], z_coords[i]
                    if i == 0:
                        speed_on = speed_save_point
                        laser_output = 0.000000
                        speed_on = speed_return
                    else:
                        speed_on = speed_save_point
                        laser_output = laser_output_save_point
                    fab_file.write(f"c\t0\t{x:.6f}\t{y:.6f}\t{z:.6f}\t{speed_on:.6f}\t{laser_output:.6f}\t0\n")
                fab_file.write(f"c\t0\t{modified_x_coords[-1]:.6f}\t{modified_y_coords[-1]:.6f}\t{min_z:.6f}\t{speed_return:.6f}\t0.000000\t0\n")
    #In case we built only a 2D polygon base, this part of the code will raise it up in slices
    elif build_polygon == 1:
        print('we build up a polygon')
        z = 0
        while z <= z_height:
            for i in range(len(x_coords)):
                    x, y = x_coords[i], y_coords[i]
                    if i == 0:
                        speed_on = speed_save_point
                        laser_output = 0.000000
                        speed_on = speed_return
                    else:
                        speed_on = speed_save_point
                        laser_output = laser_output_save_point
                    fab_file.write(f"c\t0\t{x:.6f}\t{y:.6f}\t{z:.6f}\t{speed_on:.6f}\t{laser_output:.6f}\t0\n")
            fab_file.write(f"c\t0\t{x_coords[0]:.6f}\t{y_coords[0]:.6f}\t{z:.6f}\t{speed_on:.6f}\t{laser_output:.6f}\t0\n") #line to close the polygon         
            z += z_step   
    #If we already input a finished object and we don't want to repeat it, this part of the code will run
    else:
        print('we draw the given object')
        coordinates = [(x, y, z, i) for i, (x, y, z) in enumerate(zip(x_coords, y_coords, z_coords))]

        # Sort the coordinates based on y and x values
        sorted_coordinates = sorted(coordinates, key=lambda coord: (coord[1]))

        # Iterate through the sorted coordinates and write them to the fab file
        for x, y, z, i in sorted_coordinates:
                    if i == 0:
                        speed_on = speed_save_point
                        laser_output = 0.000000
                        speed_on = speed_return
                    else:
                        speed_on = speed_save_point
                        laser_output = laser_output_save_point
                    fab_file.write(f"c\t0\t{x:.6f}\t{y:.6f}\t{z:.6f}\t{speed_on:.6f}\t{laser_output:.6f}\t0\n")
    
    if crosses == 1:    
        #kriziky
        z = 0
        mid_x = (max_x + min_x)/2
        mid_y = (max_y + min_y)/2
        while z <= max_z:
            if z == 0.100:
                pass
            else:
                fab_file.write(f"c\t0\t{mid_x:.6f}\t{mid_y:.6f}\t{z:.6f}\t{speed_return:.6f}\t0.000000\t0\n")
                fab_file.write(f"c\t0\t{(max_x+overhang_x):.6f}\t{mid_y:.6f}\t{z:.6f}\t{speed_on:.6f}\t{laser_output:.6f}\t0\n")
                fab_file.write(f"c\t0\t{(min_x-overhang_x):.6f}\t{mid_y:.6f}\t{z:.6f}\t{speed_on:.6f}\t{laser_output:.6f}\t0\n")
                fab_file.write(f"c\t0\t{mid_x:.6f}\t{mid_y:.6f}\t{z:.6f}\t{speed_return:.6f}\t0.000000\t0\n")
                fab_file.write(f"c\t0\t{(mid_x):.6f}\t{(max_y+overhang_y):.6f}\t{z:.6f}\t{speed_on:.6f}\t{laser_output:.6f}\t0\n")
                fab_file.write(f"c\t0\t{(mid_x):.6f}\t{(min_y-overhang_y):.6f}\t{z:.6f}\t{speed_on:.6f}\t{laser_output:.6f}\t0\n")
            z += cross_spacing
        #Velky kriz v strede
        z = 0.100
        long_overhang_x = 2*overhang_x
        long_overhang_y = 2*overhang_y
        fab_file.write(f"c\t0\t{mid_x:.6f}\t{mid_y:.6f}\t{z:.6f}\t{speed_return:.6f}\t0.000000\t0\n")
        fab_file.write(f"c\t0\t{(max_x+long_overhang_x):.6f}\t{mid_y:.6f}\t{z:.6f}\t{speed_on:.6f}\t{laser_output:.6f}\t0\n")
        fab_file.write(f"c\t0\t{(min_x-long_overhang_x):.6f}\t{mid_y:.6f}\t{z:.6f}\t{speed_on:.6f}\t{laser_output:.6f}\t0\n")
        fab_file.write(f"c\t0\t{mid_x:.6f}\t{mid_y:.6f}\t{z:.6f}\t{speed_return:.6f}\t0.000000\t0\n")
        fab_file.write(f"c\t0\t{(mid_x):.6f}\t{(max_y+long_overhang_y):.6f}\t{z:.6f}\t{speed_on:.6f}\t{laser_output:.6f}\t0\n")
        fab_file.write(f"c\t0\t{(mid_x):.6f}\t{(min_y-long_overhang_y):.6f}\t{z:.6f}\t{speed_on:.6f}\t{laser_output:.6f}\t0\n")  
        

# Laser settings
if __name__ == "__main__":
    with open(r'C:\Users\mitura\source\repos\Polygons\Polygons\3D_2pp_input.yaml') as file:
        input_dict = yaml.load(file, Loader=yaml.FullLoader)
        laser_output = input_dict['laser_output']
        speed_on = input_dict['speed_on']
        output_file = input_dict['output_file']
        x_repetition = input_dict['x_repetition']
        y_repetition = input_dict['y_repetition']
        spacing = input_dict['spacing']
        crosses = input_dict['crosses']
        cross_spacing = input_dict['cross_spacing']
        build_polygon = input_dict['build_polygon']
        z_height = input_dict['z_height']
        z_step = input_dict['z_step']
        overhang_x = input_dict['overhang_x']
        overhang_y = input_dict['overhang_y']
        scale_ratio = input_dict['scale_ratio']
        object_input_file = input_dict['object_input_file']
        
        
        with open(object_input_file) as file:
            polygon_data = yaml.load(file, Loader=yaml.FullLoader)
            polygon = polygon_data.get('points', [])
         
        scaled_polygon_coords = [{'x': (point['x'] * scale_ratio), 'y': point['y'] * 0.1 * scale_ratio, 'z': point['z'] * scale_ratio} for point in polygon]
        x_coords = [point['x'] for point in scaled_polygon_coords]
        y_coords = [point['y'] for point in scaled_polygon_coords]
        z_coords = [point['z'] for point in scaled_polygon_coords]

        max_x = max(x_coords)
        min_x = min(x_coords)
        max_y = max(y_coords)
        min_y = min(y_coords)
        min_z = min(z_coords)
        max_z = max(z_coords)
        
    visualize_3d_points(x_coords, y_coords, z_coords)


with open(output_file, "w") as fab_file:
    draw_contours(fab_file, x_repetition, y_repetition, build_polygon, z_height, z_step, x_coords, y_coords, z_coords, speed_on, laser_output, max_x, max_y, max_z, min_x, min_y, min_z, spacing, crosses, cross_spacing, overhang_x, overhang_y)