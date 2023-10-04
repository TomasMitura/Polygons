def draw_wall(x_coordinates, base_z, z_max, z_increment, speed_on, file_path):
    with open(file_path, "w") as fab_file:
        fab_file.write("p\t2\n")

        laser_output = 2  # Inconsequential, we are not using it

        y0 = 0.0
        y1 = 0.5

        for x0 in x_coordinates:
            z = base_z
            while z <= z_max:
                fab_file.write(f"c\t0\t{x0:.6f}\t{y0:.6f}\t{z:.6f}\t{speed_on:.6f}\t{speed_on:.6f}\t{speed_on:.6f}\t{laser_output:.6f}\t0\n")
                fab_file.write(f"c\t0\t{x0:.6f}\t{y1:.6f}\t{z:.6f}\t{speed_on:.6f}\t{speed_on:.6f}\t{speed_on:.6f}\t{laser_output:.6f}\t0\n")
                z += z_increment  # Change to minus after visualization

    print(f".fab file '{file_path}' generated successfully!")
    
#def draw_lines()
    #with open(file_path, "w") as fab_file:
        #fab_file.write("p\t2\n")
        
        #laser_output = 2
        
        

# Call the function with appropriate inputs
if __name__ == "__main__":
    x_coordinates = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]  # Add your desired x coordinates here
    z_increment = 0.005
    base_z = 0.00
    z_max = 0.30
    speed_on = 2
    file_path = r"C:\Users\mitura\Documents\Python_scripts\2pp\walls_for_lines.fab"

    draw_wall(x_coordinates, base_z, z_max, z_increment, speed_on, file_path)
