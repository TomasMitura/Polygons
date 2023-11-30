def mriezka(vert_line_length, horiz_line_length, vert_line_gap, horiz_line_gap, speed_on, speed_off, base_z, object_start_x, object_start_y, file_path):
    with open(file_path, "w") as fab_file:
        fab_file.write(f"p\t3\n")
        laser_off = 0
        laser_output = 2 #inconsequential, we are not using it
        x = object_start_x
        y = object_start_y
        while x <= horiz_line_length:
            fab_file.write(f"c\t0\t{x:.6f}\t{y:.6f}\t{base_z:.6f}\t{speed_off:.6f}\t{laser_off:.6f}\t0\n")
            z = vert_line_length
            fab_file.write(f"c\t0\t{x:.6f}\t{y:.6f}\t{z:.6f}\t{speed_on:.6f}\t{laser_output:.6f}\t0\n")
            x += horiz_line_gap
            z = base_z
        x = object_start_x
        y = object_start_y
        z = base_z
        while z <= vert_line_length:
            fab_file.write(f"c\t0\t{x:.6f}\t{y:.6f}\t{z:.6f}\t{speed_off:.6f}\t{laser_off:.6f}\t0\n")
            x = horiz_line_length
            fab_file.write(f"c\t0\t{x:.6f}\t{y:.6f}\t{z:.6f}\t{speed_on:.6f}\t{laser_output:.6f}\t0\n")
            z += vert_line_gap
            x = object_start_x
            
    print(f".fab file '{file_path}' generated successfully!")

# Call the function with appropriate inputs
if __name__ == "__main__":
    vert_line_length = 2
    horiz_line_length = 2
    vert_line_gap = 0.3
    horiz_line_gap = 0.1
    speed_on = 1
    speed_off = 200
    base_z = 0
    object_start_x = 0
    object_start_y = 0
    file_path = r"C:\Users\mitura\Documents\Python_scripts\2pp\Mriezka.fab"
    
    mriezka(vert_line_length, horiz_line_length, vert_line_gap, horiz_line_gap, speed_on, speed_off, base_z, object_start_x, object_start_y, file_path)
