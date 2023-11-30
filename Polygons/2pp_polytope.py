import yaml

def draw_contours(fab_file, x_repetition, y_repetition, spacing, x_coords, y_coords, z, speed_on, laser_output):
    speed_return = 20.0
    n = 1
    m = 1
    
    speed_save_point = speed_on
    laser_output_save_point = laser_output

    for n in range(y_repetition):
            y = [y + n * spacing for y in y_coords]
    
            for m in range(x_repetition):
                x = [x + m * spacing for x in x_coords]
                for i in range(len(x)):
                    if i == 0:
                        speed_on = speed_save_point
                        laser_output = 0.000000
                        speed_on = speed_return
                    else:
                        speed_on = speed_save_point
                        laser_output = laser_output_save_point
                    fab_file.write(f"c\t0\t{x[i]:.6f}\t{y[i]:.6f}\t{z[i]:.6f}\t{speed_on:.6f}\t{laser_output:.6f}\t0\n")

# Laser settings
if __name__ == "__main__":
    # Load input data from the first YAML file
    with open(r'C:\Users\mitura\source\repos\Polygons\Polygons\3D_2pp_input.yaml') as file:
        input_dict = yaml.load(file, Loader=yaml.FullLoader)
        laser_output = input_dict['laser_output']
        speed_on = input_dict['speed_on']
        output_file = input_dict['output_file']
        scale_ratio = input_dict['scale_ratio']
        x_repetition = input_dict['x_repetition']
        y_repetition = input_dict['y_repetition']
        spacing = input_dict['spacing']

    # Load polygon vertices from the second YAML file
    with open(r'C:\Users\mitura\Documents\Python_scripts\Objects\Deconstructed_cube.yaml') as file:
        polygons_data = yaml.load(file, Loader=yaml.FullLoader)

    # Iterate over polygons and draw them
    with open(output_file, "w") as fab_file:
        fab_file.write("p\t2\n")
        for polygon_key, polygon_coords in polygons_data.items():
            scaled_polygon_coords = [{'x': point['x'] * scale_ratio, 'y': point['y'] * scale_ratio, 'z': point['z'] * scale_ratio} for point in polygon_coords]
            x_coords = [point['x'] for point in scaled_polygon_coords]
            y_coords = [point['y'] for point in scaled_polygon_coords]
            z = [point['z'] for point in scaled_polygon_coords]
            draw_contours(fab_file, x_repetition, y_repetition, spacing, x_coords, y_coords, z, speed_on, laser_output)
