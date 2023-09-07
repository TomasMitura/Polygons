from polygenerator import random_polygon
import matplotlib.pyplot as plt

polygon = random_polygon(num_points=10)
polygon.append(polygon[0])

min_x = min(p[0] for p in polygon)
max_x = max(p[0] for p in polygon)
min_y = min(p[1] for p in polygon)
max_y = max(p[1] for p in polygon)

# Plot the polygon
polygon_x = [p[0] for p in polygon]
polygon_y = [p[1] for p in polygon]

# Plot the bounding box
bounding_box_x = [min_x, max_x, max_x, min_x, min_x]
bounding_box_y = [min_y, min_y, max_y, max_y, min_y]

plt.plot(polygon_x, polygon_y, marker='o', linestyle='-', color='blue', label='Polygon')
plt.plot(bounding_box_x, bounding_box_y, linestyle='--', color='green', label='Bounding Box')

plt.xlabel('X')
plt.ylabel('Y')
plt.title('Polygon and Bounding Box')
plt.legend()
plt.grid()
plt.show()
