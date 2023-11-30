import yaml
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Line3DCollection

obj_file_path = r"C:\Users\mitura\Documents\Python_scripts\Objects\Array_for_Learning.obj"

with open(obj_file_path, 'r') as obj_file:
    lines = obj_file.readlines()

# Lists to store vertices
vertices = []

for line in lines:
    words = line.split()
    if not words:
        continue

    if words[0] == 'v':
        x, y, z = map(float, words[1:])
        vertices.append([x, y, z])

# Create a list to store the point data
point_data = []

# Iterate over the vertices and add them to the list
for vertex in vertices:
    x, y, z = vertex
    point_data.append({"x": x, "y": y, "z": z})

points_list = [
    f"- {{x: {x}, y: {y}, z: {z}}}" for x, y, z in vertices
]

# Specify the output YAML file path
output_yaml_file = r"C:\Users\mitura\Documents\Python_scripts\Objects\TestPoints.yaml"

# Write the YAML data to the file
with open(output_yaml_file, 'w') as yaml_file:
    yaml_file.write("points:\n")
    yaml_file.write("\n".join(points_list))

# Extract coordinates for visualization
x_coords = [vertex[0] for vertex in vertices]
y_coords = [vertex[1] for vertex in vertices]
z_coords = [vertex[2] for vertex in vertices]

# Plot the points
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(x_coords, y_coords, z_coords, c='b', marker='o')

# Set axis labels
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

plt.show()