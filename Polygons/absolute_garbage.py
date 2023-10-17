import numpy as np
import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

#code done based on this
#https://www.scratchapixel.com/lessons/3d-basic-rendering/ray-tracing-rendering-a-triangle/ray-triangle-intersection-geometric-solution.html  

def calculate_normal(vertex0, vertex1, vertex2):
    edge1 = vertex1 - vertex0
    edge2 = vertex2 - vertex0
    normal = np.cross(edge1, edge2)
    return normal

# Function to check if a point is inside a triangle
def is_point_inside_triangle(vertex0, vertex1, vertex2, P, N):
    edge0 = vertex1 - vertex0
    edge1 = vertex2 - vertex1
    edge2 = vertex0 - vertex2

    C0 = P - vertex0
    C1 = P - vertex1
    C2 = P - vertex2

    cross0 = np.cross(edge0, C0)
    cross1 = np.cross(edge1, C1)
    cross2 = np.cross(edge2, C2)

    dot0 = np.dot(N, cross0)
    dot1 = np.dot(N, cross1)
    dot2 = np.dot(N, cross2)

    return dot0 > 0 and dot1 > 0 and dot2 > 0

# Function to calculate the intersection point of a ray and a plane
def ray_plane_intersection(ray_origin, ray_direction, plane_normal, D):
    denominator = np.dot(plane_normal, ray_direction)

    # Check if the denominator is very close to zero (avoiding division by almost zero)
    if np.abs(denominator) < 1e-9:
        return None, None

    t = -(np.dot(plane_normal, ray_origin) + D) / denominator

    # Calculate the intersection point
    intersection_point = ray_origin + t * ray_direction

    return intersection_point, denominator
        

# Load the vertices and faces from the OBJ file
obj_file_path = r'C:\Users\mitura\Documents\Python_scripts\Objects\test_object.obj'

vertices = []
triangles = []

with open(obj_file_path, 'r') as file:
    lines = file.readlines()
    for line in lines:
        parts = line.strip().split(' ')
        if parts[0] == 'v':
            vertex = np.array([float(parts[1]), float(parts[2]), float(parts[3])])
            vertices.append(vertex)
        elif parts[0] == 'f':
            # Convert vertex indices to integers and subtract 1 (0-based indices)
            indices = [int(part) - 1 for part in parts[1:]]
            triangles.append(indices)

# Calculate normals for each triangle
triangle_normals = [calculate_normal(vertices[i], vertices[j], vertices[k]) for i, j, k in triangles]

# Define step size for rasterization
step_size = 1.5

tolerance = 1e-6
ray_direction = np.array([0.0, 0.0, 1.0])

# Initialize a list to store intersection points
intersection_points = []

# Iterate through triangles and find intersection points with the XY plane
for i, triangle in enumerate(triangles):
    vertex_indices = triangle
    vertex0, vertex1, vertex2 = [vertices[i] for i in vertex_indices]
    triangle_normal = triangle_normals[i]
    #calculate bounding box
    max_x = max(vertex[0] for vertex in vertices)
    max_y = max(vertex[1] for vertex in vertices)
    min_x = min(vertex[0] for vertex in vertices)
    min_y = min(vertex[1] for vertex in vertices)
    max_z = max(vertex[2] for vertex in vertices)
    min_z = min(vertex[2] for vertex in vertices)
    x_range = np.arange(min_x, max_x + step_size, step_size)
    y_range = np.arange(min_y, max_y + step_size, step_size)
    xy_plane_points = [(x, y, 0.0) for x in x_range for y in y_range]
     
    # Find the intersection points
    for point in xy_plane_points:
        ray_origin = np.array(point)

        # Find the intersection point between the ray and the plane
        intersection_point, denominator = ray_plane_intersection(ray_origin, ray_direction, triangle_normal, -np.dot(triangle_normal, vertex0))
         
        if intersection_point is not None:
            is_inside = is_point_inside_triangle(vertex0, vertex1, vertex2, intersection_point, triangle_normal)
            if is_inside:
                if abs(denominator) > 1e-6:
                    intersection_points.append(intersection_point)


fab_file.write(f"c\t0\t{x1:.6f}\t{y1:.6f}\t0.000000\t{speed_off:.6f}\t{speed_off:.6f}\t{speed_off:.6f}\t0.000000\t0\n")
fab_file.write(f"c\t1\t{x2:.6f}\t{y2:.6f}\t0.000000\t{speed_on:.6f}\t{speed_on:.6f}\t{speed_on:.6f}\t{laser_output:.6f}\t0\n")        
    
     


# Convert intersection points to a numpy array for plotting
intersection_points = np.array(intersection_points)

# Plot the triangle and intersection points
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')


# Plot the intersection points
ax.scatter(intersection_points[:, 0], intersection_points[:, 1], intersection_points[:, 2], color='red', label='Intersection Points')

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.legend()
plt.show()
