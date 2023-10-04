def draw_pyramid(base_z, z_increment, xy_increment, speed_on, file_path):
    with open(file_path, "w") as fab_file:
        fab_file.write(f"p\t2\n")

        laser_output = 2 #inconsequential, we are not using it
        z = base_z
        x0 = 0.0
        y0 = 0.0
        x1 = 0.4
        y1 = 0.4
        while (abs(x1)-abs(x0)) > 0.01:
            fab_file.write(f"c\t0\t{x0:.6f}\t{y0:.6f}\t{z:.6f}\t{speed_on:.6f}\t{speed_on:.6f}\t{speed_on:.6f}\t{laser_output:.6f}\t0\n")
            fab_file.write(f"c\t0\t{x0:.6f}\t{y1:.6f}\t{z:.6f}\t{speed_on:.6f}\t{speed_on:.6f}\t{speed_on:.6f}\t{laser_output:.6f}\t0\n")
            fab_file.write(f"c\t0\t{x1:.6f}\t{y1:.6f}\t{z:.6f}\t{speed_on:.6f}\t{speed_on:.6f}\t{speed_on:.6f}\t{laser_output:.6f}\t0\n")
            fab_file.write(f"c\t0\t{x1:.6f}\t{y0:.6f}\t{z:.6f}\t{speed_on:.6f}\t{speed_on:.6f}\t{speed_on:.6f}\t{laser_output:.6f}\t0\n")
            x1 += -(xy_increment)
            y1 += -(xy_increment)
            x0 += xy_increment
            y0 += xy_increment 
            z+= z_increment #change to minus after vizualization

    
    print(f".fab file '{file_path}' generated successfully!")

# Call the function with appropriate inputs
if __name__ == "__main__":
    z_increment = 0.005
    xy_increment = 0.005
    base_z = 1.08
    speed_on = 6
    file_path = r"C:\Users\mitura\Documents\Python_scripts\2pp\pyramid_6mms.fab"
    
    draw_pyramid(base_z, z_increment, xy_increment, speed_on, file_path)
