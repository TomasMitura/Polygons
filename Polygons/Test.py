import matplotlib.pyplot as plt
import sys

def draw_point(pt):
    x, y = pt
    plt.plot(x, y, "go", markersize=5)

def draw_polygon(edges):
    for edge in edges:
        x_coords, y_coords = zip(*edge)
        plt.plot(x_coords, y_coords, "b-")

def generate_intersection(line_a, line_b):
    pt1, pt2 = line_a
    pt3, pt4 = line_b
    x1, y1 = pt1
    x2, y2 = pt2
    x3, y3 = pt3
    x4, y4 = pt4

    divisor = ((x1 - x2)*(y3 - y4) - (y1 - y2)*(x3 - x4))
    if divisor == 0:
        return None

    t = ((x1 - x3)*(y3 - y4) - (y1 - y3)*(x3 - x4)) / divisor
    if 0 <= t and t <= 1:
        return (round(x1 + t*(x2 - x1), 6), round(y1 + t*(y2 - y1), 6))
    return None

def draw_contours(edges, fab_file):
    intersection_points = []  # To store intersection points
    
    for y_coord in range(0, 100): #put back to 1000
        y_coord /= 100 #put back to 1000
        horizontal_line = ((0, y_coord), (1, y_coord))
        for edge in edges:
            intersection = generate_intersection(edge, horizontal_line)
            if intersection is not None:
                draw_point(intersection)
                intersection_points.append(intersection)
            if edge[0][1] == edge[1][1] == y_coord:
                intersection_points.extend([(round(edge[0][0], 6), round(edge[0][1], 6)),
                                            (round(edge[1][0], 6), round(edge[1][1], 6))])
    
    # Sort intersection points based on y-coordinates
    intersection_points.sort(key=lambda point: point[1])
    
    for i in range(0, len(intersection_points), 2):
        x1, y1 = intersection_points[i]
        x2, y2 = intersection_points[i + 1]
        fab_file.write(f"c\t0\t{x1:.6f}\t{y1:.6f}\t0.000000\t{speed_off:.6f}\t{speed_off:.6f}\t{speed_off:.6f}\t0.000000\t0\n")
        fab_file.write(f"c\t1\t{x2:.6f}\t{y2:.6f}\t0.000000\t{speed_on:.6f}\t{speed_on:.6f}\t{speed_on:.6f}\t{laser_output:.6f}\t0\n")

# Star Polygon
polygon = [
    (0.5, 1.0),
    (0.61, 0.69),
    (0.91, 0.7),
    (0.69, 0.49),
    (0.8, 0.2),
    (0.5, 0.4),
    (0.2, 0.2),
    (0.31, 0.49),
    (0.09, 0.7),
    (0.39, 0.69),
    (0.7, 0.45),
    (0.98, 0.23),
    (0.11, 0.64),
    (0.69, 0.76),
    (0.48, 0.11),
    (0.97, 0.55),
    (0.29, 0.69),
    (0.37, 0.97),
    (0.63, 0.34),
    (0.22, 0.42),
]
edges = list(zip(polygon, polygon[1:] + polygon[:1]))

# Laser settings
if __name__ == "__main__":
    speed_off = float(sys.argv[1])
    speed_on = float(sys.argv[2])
    laser_output = float(sys.argv[3])

output_file = r"C:\Users\mitura\Documents\Python_scripts\Polygon\Polygon_Arg_test.fab"
with open(output_file, "w") as fab_file:
    draw_contours(edges, fab_file)

plt.figure()

# Draw the polygon outline
draw_polygon(edges)

# Show the plot
plt.axis('equal')  # Set aspect ratio to equal for a consistent scale
plt.show()
