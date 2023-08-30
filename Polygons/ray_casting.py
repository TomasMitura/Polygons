import matplotlib.pyplot as plt
import numpy as np
from polygenerator import random_polygon

# Generate a random polygon
num_points = 20
polygon = random_polygon(num_points=num_points)
polygon.append(polygon[0])  # Close the polygon

# Separate x and y values for plotting the polygon perimeter
x_coords, y_coords = zip(*polygon)

# Plotting the polygon perimeter
plt.figure(figsize=(8, 6))
plt.plot(x_coords, y_coords, marker='o', color='blue', label='Polygon Perimeter')

# Initialize empty list to store perimeter points
perimeter_points = []

# Define ray casting parameters
min_x = min(x_coords)
max_x = max(x_coords)
min_y = min(y_coords)
max_y = max(y_coords)
interval = 0.01

# Iterate through x values and incrementally increase y
for x in np.arange(min_x, max_x, interval):
    y_intersections = []
    for i in range(num_points):
        x1, y1 = polygon[i]
        x2, y2 = polygon[i + 1]

        if (y1 > min_y and y2 <= max_y) or (y1 < min_y and y2 >= min_y):
            y_intersection = y1 + (x - x1) * (y2 - y1) / (x2 - x1)
            if min(y1, y2) <= y_intersection <= max(y1, y2):
                y_intersections.append(y_intersection)

    if y_intersections:
        y_intersection = min(y_intersections)
        perimeter_points.append((x, y_intersection))

# Extract x and y coordinates of perimeter points
perimeter_x, perimeter_y = zip(*perimeter_points)

# Plot the perimeter points
plt.plot(perimeter_x, perimeter_y, color='red', label='Perimeter')
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.title('Perimeter of Random Polygon using Ray Casting')
plt.legend()
plt.grid(True)
plt.show()
