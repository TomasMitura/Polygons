import os
import matplotlib.pyplot as plt
import pandas as pd

# Directory path containing the CSV files
directory_path = "C:/Users/mitura/Documents/Dektak"

# List of CSV file names and corresponding legend labels
csv_files = [
    #("L9_z500_w02_Y-scan.csv", "z 500um, w 02um"),
    #("L2_z100.csv", "z 100 um"),
    #("L2_z200.csv", "z 200 um"),
    #("L2_z300.csv", "z 300 um"),
    #("L2_z400.csv", "z 400 um"),
    #("L3_w01.csv", "w 01um"),
    #("L3_w02.csv", "w 02um"),
    #("L2_z500.csv", "z 500 um"),
    ("L3_z500_w02.csv", "z 500um, w 0.2 um"),
    #("L10_4x_2mms_low_energy.csv", "4x low energy 2 mms"),
    #("L10_4x_repeat_same_line.csv", "4x repeat same line"),
    #("L10_4x_8mms.csv", "4x 8 mm/s"),
    #("L10_8x_16mms.csv", "8x 16 mm/s"),
    #("L12_4x_repeat_slow.csv", "4x 2 mm/s"),
    #("L12_4x_repeat_fast.csv", "4x 8 mm/s"),
    #("L12_4x_repeat_same_lines.csv", "4x repeat same lines"),
    #("L12_8x_repeat.csv", "8x 16 mm/s"),
    #("L9_kanaliky_right_bez_stredu.csv", "kanaliky - v lavo"),
    #("L9_kanaliky_left_bez_stredu.csv", "kanaliky - hlbka 65, 75, 85, 95 um"),
    ("L13_8x_repeat_same_lines.csv", "8x 16 mm/s same lines")
    #("L13_w1um_2mms.csv", "1x 2 mm/s - 25.09. - depth 100 um"), 
    #("L15A_8x_repeat_1develop_AZ326.csv", "8x 16 mm/s, AZ326 - 28.09. - depth 70 um"),
    #("L15B_8x_repeat_mad532s.csv", "8x 16 mm/s, mad532-S - 28.09. - depth 70 um"),
    #("L16_vertical_scan.csv", "1 2 mm/s, mad532-S - 2.10. - depth 75 um")
    #("P2_control_sample.csv", "Control sample - exposure 1, development 1"),
    #("P2_4x_repeat_first_dev.csv", "4x repeat - exposure 1, development 1")
    #("P2_4x_repeat_second_dev_vertical_middle.csv", "4x repeat, vertical stripe, 1 exposure 2 exposures, 2 developments"),
    #("P2_4x_repeat_second_dev_vertical_left_vertical.csv", "4x repeat, horizontal stripe, 1 exposure, 2 developments")
    #("P2_4x_repeat_second_dev_horizontal.csv", "4x repeat, 4x repeat, horizontal stripe, 1 exposure, 2 exposures, 2 developments. Horizontal scan")
    #("V1_X_80um.csv" ,"X 80um"),
    #("V1_X_91um.csv", "X 91um"),
    #("V1_Y_80um.csv", "Y 80um"),
    #("V1_Y_91um.csv", "Y 91um"),
    #("V3_w05um_4mms.csv", "141um, hatch = 0.5 um, spd = 4 mm/s"),
    #("V3_4x_repeat_8mms.csv", "104um, 4x repeat, spd = 8 mm/s ")
    #("V8_5uW.csv", "48um"),
    #("V8_7-5uW.csv", "58um"),
    #("V8_10uW.csv", "68um"),
    #("V8_15uW.csv", "81um"),
    #("V8_20uW.csv", "90um")
    #("V8_15uW_z-100.csv", "80um, defocused: z = -100um"),
    #("V8_15uW_z-300.csv", "80um, defocused, z = -300um"),
    #("V8_15uW_z-500.csv", "80um, defocused, z = -500um")
    ]
plt.figure(figsize=(10, 6))

for csv_file, legend_label in csv_files:
    # Construct the full file path
    full_path = os.path.join(directory_path, csv_file)
    
    # Read data from CSV file using Pandas
    data = pd.read_csv(full_path, header=None, names=["Distance [um]", "Depth [nm]"])
    
    # Plot data
    plt.plot(data["Distance [um]"], data["Depth [nm]"], label=legend_label)

plt.xlabel("Distance [um]")
plt.ylabel("Depth [nm]")
plt.legend()
plt.grid()
plt.show()
