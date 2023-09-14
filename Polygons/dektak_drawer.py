import os
import matplotlib.pyplot as plt
import pandas as pd

# Directory path containing the CSV files
directory_path = "C:/Users/mitura/Documents/Dektak"

# List of CSV file names and corresponding legend labels
csv_files = [
    ("L9_z500_w02_Y-scan.csv", "z 500um, w 02um"),
    #("L2_z100.csv", "z 100 um"),
    #("L2_z200.csv", "z 200 um"),
    #("L2_z300.csv", "z 300 um"),
    #("L2_z400.csv", "z 400 um"),
    #("L3_w01.csv", "w 01um"),
    #("L3_w02.csv", "w 02um"),
    #("L2_z500.csv", "z 500 um"),
    #("L3_z500_w02.csv", "z 500um, w 1um"),
    ("L10_4x_2mms_low_energy.csv", "4x low energy 2 mms"),
    ("L10_4x_repeat_same_line.csv", "4x repeat same line"),
    ("L10_4x_8mms.csv", "4x 8 mms"),
    ("L10_8x_16mms.csv", "8x 16 mms")
    
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
