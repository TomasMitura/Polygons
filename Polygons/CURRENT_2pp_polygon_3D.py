import matplotlib.pyplot as plt
import yaml
import math

def draw_contours(fab_file, x_repetition, y_repetition, x_coords, y_coords, z_coords, speed_on, laser_output, max_x, max_y, max_z, min_x, min_y, min_z, spacing, kriziky):
    fab_file.write("p\t2\n")
    x_move = max_x + spacing
    y_move = max_y + spacing
    n = 1
    m = 1
    speed_return = 80.0
    speed_save_point = speed_on
    laser_output_save_point = laser_output
    
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
            if y_repetition > 1 or x_repetition > 1:
                fab_file.write(f"c\t0\t{modified_x_coords[-1]:.6f}\t{modified_y_coords[-1]:.6f}\t{min_z:.6f}\t{speed_return:.6f}\t0.000000\t0\n")
    if kriziky == 1:    
        #kriziky
        z = 0
        mid_x = (max_x + min_x)/2
        mid_y = (max_y + min_y)/2
        overhang_x = 0.05
        overhang_y = 0.05
        while z <= max_z:
            fab_file.write(f"c\t0\t{mid_x:.6f}\t{mid_y:.6f}\t{z:.6f}\t{speed_return:.6f}\t0.000000\t0\n")
            fab_file.write(f"c\t0\t{(max_x+overhang_x):.6f}\t{mid_y:.6f}\t{z:.6f}\t{speed_on:.6f}\t{laser_output:.6f}\t0\n")
            fab_file.write(f"c\t0\t{(min_x-overhang_x):.6f}\t{mid_y:.6f}\t{z:.6f}\t{speed_on:.6f}\t{laser_output:.6f}\t0\n")
            fab_file.write(f"c\t0\t{mid_x:.6f}\t{mid_y:.6f}\t{z:.6f}\t{speed_return:.6f}\t0.000000\t0\n")
            fab_file.write(f"c\t0\t{(mid_x):.6f}\t{(max_y+overhang_y):.6f}\t{z:.6f}\t{speed_on:.6f}\t{laser_output:.6f}\t0\n")
            fab_file.write(f"c\t0\t{(mid_x):.6f}\t{(min_y-overhang_y):.6f}\t{z:.6f}\t{speed_on:.6f}\t{laser_output:.6f}\t0\n")
            z += 0.05
        #Velky kriz v strede
        z = max_z/2
        overhang_x = 0.15
        overhang_y = 0.15
        fab_file.write(f"c\t0\t{mid_x:.6f}\t{mid_y:.6f}\t{z:.6f}\t{speed_return:.6f}\t0.000000\t0\n")
        fab_file.write(f"c\t0\t{(max_x+overhang_x):.6f}\t{mid_y:.6f}\t{z:.6f}\t{speed_on:.6f}\t{laser_output:.6f}\t0\n")
        fab_file.write(f"c\t0\t{(min_x-overhang_x):.6f}\t{mid_y:.6f}\t{z:.6f}\t{speed_on:.6f}\t{laser_output:.6f}\t0\n")
        fab_file.write(f"c\t0\t{mid_x:.6f}\t{mid_y:.6f}\t{z:.6f}\t{speed_return:.6f}\t0.000000\t0\n")
        fab_file.write(f"c\t0\t{(mid_x):.6f}\t{(max_y+overhang_y):.6f}\t{z:.6f}\t{speed_on:.6f}\t{laser_output:.6f}\t0\n")
        fab_file.write(f"c\t0\t{(mid_x):.6f}\t{(min_y-overhang_y):.6f}\t{z:.6f}\t{speed_on:.6f}\t{laser_output:.6f}\t0\n")  
        

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
        kriziky = input_dict['kriziky']
        
    with open(r'C:\Users\mitura\Documents\Python_scripts\Objects\CubeMash.yaml') as file:
        polygon_data = yaml.load(file, Loader=yaml.FullLoader)
        polygon = polygon_data.get('points', [])
         
    x_coords = [point['x'] for point in polygon]
    y_coords = [point['y'] for point in polygon]
    z_coords = [point['z'] for point in polygon]

    max_x = max(x_coords)
    min_x = min(x_coords)
    max_y = max(y_coords)
    min_y = min(y_coords)
    min_z = min(z_coords)
    max_z = max(z_coords)


with open(output_file, "w") as fab_file:
    draw_contours(fab_file, x_repetition, y_repetition, x_coords, y_coords, z_coords, speed_on, laser_output, max_x, max_y, max_z, min_x, min_y, min_z, spacing, kriziky)