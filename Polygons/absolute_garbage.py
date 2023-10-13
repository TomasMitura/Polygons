import numpy as np
import math

#https://www.scratchapixel.com/lessons/3d-basic-rendering/ray-tracing-rendering-a-triangle/ray-triangle-intersection-geometric-solution.html           

def calculate_barycentric_coordinates(point, vertex0, vertex1, vertex2):
    v0v1 = vertex1 - vertex0
    v0v2 = vertex2 - vertex0
    v1v2 = vertex2 - vertex1
    area = np.linalg.norm(np.cross(v0v1, v0v2))  # Area of the triangle

    alpha = np.linalg.norm(np.cross(v1v2, point - vertex2)) / area
    beta = np.linalg.norm(np.cross(v0v2, point - vertex0)) / area
    gamma = np.linalg.norm(np.cross(v0v1, point - vertex1)) / area

    return alpha, beta, gamma

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

def ray_plane_intersection(ray_origin, ray_direction, plane_normal, D):
    denominator = np.dot(plane_normal, ray_direction)
    
    # Check if the ray and plane are not parallel
    if abs(denominator) > 1e-6:
        # Calculate the intersection parameter 't'
        t = -(np.dot(plane_normal, ray_origin) + D) / denominator

        # Calculate the intersection point
        intersection_point = ray_origin + t * ray_direction

        return intersection_point
    else:
        return None  # Ray and plane are parallel
    

def calculate_plane(vertex0, normal):
    # Normalize the normal vector (create a unit vector)
    normal_magnitude = np.linalg.norm(normal)
    if normal_magnitude != 0:
        normal = normal / normal_magnitude
    else:
        print("Cannot normalize a zero vector.")
        return None

    # Calculate D using the dot product between the normal vector and vertex0
    D = -np.dot(normal, vertex0)
    return normal, D

def trial_plane_intersection(vertex0, vertex1, vertex2):
   edge_A = vertex1 - vertex0
   edge_B = vertex2 - vertex0
   normal = np.cross(edge_A, edge_B)
   normal_magnitude = np.linalg.norm(normal)
   if normal_magnitude != 0:
        # Normalize the normal vector (create a unit vector)
        normal = normal / normal_magnitude
        print("Normalized Normal:", normal)
   else:
        print("Cannot normalize a zero vector.")
   return normal

vertex0 = np.array([2.0, 0.0, 0.0])
vertex1 = np.array([0.0, 2.0, 0.0])
vertex2 = np.array([0.0, 0.0, 2.0])
max_x = max(vertex0[0], vertex1[0], vertex2[0])
max_y = max(vertex0[1], vertex1[1], vertex2[1])
max_z = max(vertex0[2], vertex1[2], vertex2[2])
# Define step size for rasterization
step_size = 0.1

# Rasterize the XY plane within the box
x_range = np.arange(0, max_x + step_size, step_size)
y_range = np.arange(0, max_y + step_size, step_size)
xy_plane_points = [(x, y, 0.0) for x in x_range for y in y_range]


normal = trial_plane_intersection(vertex0, vertex1, vertex2)

if normal is not None:
    # Calculate the plane equation
    plane_normal, D = calculate_plane(vertex0, normal)
    A, B, C = plane_normal
    print("Plane Equation: {}x + {}y + {}z = {}".format(A, B, C, D))
else:
    print("Plane calculation failed.")

for point in xy_plane_points:
    ray_origin = np.array(point)
    ray_direction = np.array([0.0, 0.0, 1.0])

    # Find the intersection point between the ray and the plane
    intersection_point = ray_plane_intersection(ray_origin, ray_direction, plane_normal, D)
    
    if intersection_point is not None:
        is_inside = is_point_inside_triangle(vertex0, vertex1, vertex2, intersection_point, plane_normal)
        if is_inside:
            print("Intersection point is inside the triangle.", intersection_point)
            # Calculate barycentric coordinates
            alpha, beta, gamma = calculate_barycentric_coordinates(intersection_point, vertex0, vertex1, vertex2)
            print("Barycentric Coordinates (alpha, beta, gamma):", alpha, beta, gamma)

            # Interpolate and print the intersection point using barycentric coordinates
            interpolated_point = alpha * vertex0 + beta * vertex1 + gamma * vertex2
            print("Interpolated Intersection Point:", interpolated_point)
        else:
            print("Intersection point is outside the triangle.")
    else:
        print("No intersection between the ray and the plane.")
