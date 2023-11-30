import numpy as np
import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.interpolate import interp1d
import pandas as pd
import yaml
from scipy.spatial import ConvexHull


#code done based on this
#https://www.scratchapixel.com/lessons/3d-basic-rendering/ray-tracing-rendering-a-triangle/ray-triangle-intersection-geometric-solution.html  

def calculate_bounding_box(vertices, step_size_x, step_size_y):
    max_x = max(vertex[0] for vertex in vertices)
    max_y = max(vertex[1] for vertex in vertices)
    min_x = min(vertex[0] for vertex in vertices)
    min_y = min(vertex[1] for vertex in vertices)
    max_z = max(vertex[2] for vertex in vertices)
    min_z = min(vertex[2] for vertex in vertices)
    x_range = np.arange(min_x, max_x + step_size_x, step_size_x)
    y_range = np.arange(min_y, max_y + step_size_y, step_size_y)
    xy_plane_points = [(x, y, 0.0) for x in x_range for y in y_range]
    return xy_plane_points

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
        
if __name__ == "__main__":
    with open(r'C:\Users\mitura\source\repos\Polygons\Polygons\1pp_ray_triangle_input.yaml') as file:
        input_dict = yaml.load(file, Loader=yaml.FullLoader)
        obj_file_path = input_dict['obj_file_path']
        scale_factor = input_dict['scale_factor']
        step_size_x = input_dict['step_size_x']
        step_size_y = input_dict['step_size_y']
        tolerance = input_dict['tolerance']
        speed_off = input_dict['speed_off']
        base_speed = input_dict['base_speed']
        slow_speed = input_dict['slow_speed']
        output_file = input_dict['output_file']
        depth_file = input_dict['depth_file']

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
    print('Finished reading the object')

vertices = [vertex * scale_factor for vertex in vertices]
# Calculate normals for each triangle
triangle_normals = [calculate_normal(vertices[i], vertices[j], vertices[k]) for i, j, k in triangles]

ray_direction = np.array([0.0, 0.0, 1.0])

# Initialize a list to store intersection points
intersection_points = []
n = 0
m = 0
j = 0
k = 0
# Iterate through triangles and find intersection points with the XY plane
for i, triangle in enumerate(triangles):
    vertex_indices = triangle
    vertex0, vertex1, vertex2 = [vertices[i] for i in vertex_indices]
    triangle_normal = triangle_normals[i]
    
    # Calculate the bounding box for the current triangle
    max_x = max(vertex[0] for vertex in [vertex0, vertex1, vertex2])
    max_y = max(vertex[1] for vertex in [vertex0, vertex1, vertex2])
    min_x = min(vertex[0] for vertex in [vertex0, vertex1, vertex2])
    min_y = min(vertex[1] for vertex in [vertex0, vertex1, vertex2])
    
    x_range = np.arange(min_x, max_x + step_size_x, step_size_x)
    y_range = np.arange(min_y, max_y + step_size_y, step_size_y)
    n+=1
    print('Found bounding box'+str(n))
    # Iterate through points within the bounding box of the current triangle
    for x in x_range:
        for y in y_range:
            ray_origin = np.array([x, y, 0.0])
            intersection_point, denominator = ray_plane_intersection(ray_origin, ray_direction, triangle_normal, -np.dot(triangle_normal, vertex0))
            
            if intersection_point is not None:
                is_inside = is_point_inside_triangle(vertex0, vertex1, vertex2, intersection_point, triangle_normal)
                
                if is_inside and abs(denominator) > 1e-6:
                    intersection_points.append(intersection_point)

# Convert intersection points to a numpy array for plotting
intersection_points = np.round(intersection_points, 4)
edges = set()
vertices = []

# Iterate through triangles and add their vertices and edges
for triangle in triangles:
    for i in range(3):
        vertex1, vertex2 = triangle[i], triangle[(i + 1) % 3]
        edge = tuple(sorted([vertex1, vertex2]))
        edges.add(edge)
        if vertex1 not in vertices:
            vertices.append(vertex1)
        if vertex2 not in vertices:
            vertices.append(vertex2)

# Initialize a list for outer edge points
outer_edge_points = []

# Iterate through triangles and check if each edge is unique
for triangle in triangles:
    for i in range(3):
        vertex1, vertex2 = triangle[i], triangle[(i + 1) % 3]
        edge = tuple(sorted([vertex1, vertex2]))
        if list(edge) in edges and sum(edge in t for t in edges) == 1:
            # This edge is unique and belongs to an outer edge
            outer_edge_points.append(vertex1)
            outer_edge_points.append(vertex2)

print(outer_edge_points)

# Group intersection points with the same y and z coordinates
# max_x_diff = 4 * step_size_x  # Define the maximum allowed difference in x-coordinates
# unique_yz = np.unique(intersection_points[:, 1:], axis=0)
# laser_coordinates = []

# for yz in unique_yz:
#     mask = (intersection_points[:, 1] == yz[0]) & (intersection_points[:, 2] == yz[1])
#     group_points = intersection_points[mask]
#     group_points = group_points[np.argsort(group_points[:, 0])]

#     min_x = group_points[0, 0]
#     max_x = group_points[0, 0]

#     for i in range(1, len(group_points)):
#         x = group_points[i, 0]
#         if x - max_x > max_x_diff:
#             # If the x-coordinate is more than 4 * step_size_x from the previous point,
#             # consider this as a new group
#             laser_coordinates.append([min_x, yz[0], yz[1]])
#             min_x = x
#             # Append the maximum x before moving to the next group
#             laser_coordinates.append([max_x, yz[0], yz[1]])
#         max_x = x

#     # Append both min_x and max_x for this group
#     laser_coordinates.append([min_x, yz[0], yz[1]])
#     laser_coordinates.append([max_x, yz[0], yz[1]])

# # Sort laser coordinates by y and z coordinates
# laser_coordinates = sorted(laser_coordinates, key=lambda x: (x[1], x[2]))

# df = pd.read_excel(depth_file)
# # Extract energy and depth columns from the DataFrame
# energy_data = df["Voltage"].values
# depth_data = df["Depth"].values
# laser_output = 2.0 #just initiating the variable, its value is set during writing
# # Create an interpolation function
# interp_func = interp1d(depth_data, energy_data, kind='linear', fill_value=(energy_data[0], energy_data[-1])) 

# #writing g-code for uFab into a .fab file
# with open(output_file, "w") as fab_file:
#     fab_file.write(f"p\t1\n")
#     for i in range(0, len(laser_coordinates)-1, 2):
#         x1, y1, z1 = laser_coordinates[i]
#         x2, y2, z2 = laser_coordinates[i + 1]
        
#         depth = 100-(z2*100)
#         laser_output = interp_func(depth)
#         if (x2 - x1) < 0.09:
#             speed_on = slow_speed
#             laser_output = ((laser_output - 0.5)/(base_speed/slow_speed))+0.5
#         else:
#             speed_on = base_speed
#         fab_file.write(f"c\t0\t{x1:.6f}\t{y1:.6f}\t0.000000\t{speed_off:.6f}\t0.000000\t0\n")
#         fab_file.write(f"c\t1\t{x2:.6f}\t{y2:.6f}\t0.000000\t{speed_on:.6f}\t{laser_output:.6f}\t0\n")
#         previous_y = y1

# Prompt the user for input
user_input = input("Do you want to visualize the points (y/n)? ")

# Check if the user wants to visualize the points
if user_input.lower() == 'y':
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Plot the laser coordinates
    intersection_points = np.array(intersection_points)
    ax.scatter(intersection_points[:, 0], intersection_points[:, 1], intersection_points[:, 2], color='red', label='Laser Coordinates')

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.legend()
    plt.show()

    # fig = plt.figure()
    # ax = fig.add_subplot(111, projection='3d')

    # # Plot the laser coordinates
    # laser_coordinates = np.array(laser_coordinates)
    # ax.scatter(laser_coordinates[:, 0], laser_coordinates[:, 1], laser_coordinates[:, 2], color='blue', label='Laser Coordinates')

    # ax.set_xlabel('X')
    # ax.set_ylabel('Y')
    # ax.set_zlabel('Z')
    # ax.legend()
    # plt.show()

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Plot the outer edge points
    ax.scatter([point[0] for point in outer_edge_points], [point[1] for point in outer_edge_points], [point[2] for point in outer_edge_points], color='green', label='Outer Edge Points')

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.legend()
    plt.show()
else:
    print("Visualization skipped.")

