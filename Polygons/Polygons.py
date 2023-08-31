from polygenerator import random_polygon
import matplotlib.pyplot as plt

def draw_point(pt):
    x, y = pt
    plt.plot(x, y, "go", markersize=5)

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

def draw_contours(edges, output_file):
    intersection_points = []  # To store intersection points
    
    for y_coord in range(0, 1000):
        y_coord /= 1000
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
    
    # Write intersection points to the output file
    with open(output_file, "w") as f:
        i = 0
        while i + 1 < len(intersection_points):
            x1, y1 = intersection_points[i]
            x2, y2 = intersection_points[i + 1]
            f.write(f"{x1:.6f}, {y1:.6f}, {x2:.6f}, {y2:.6f}\n")
            i += 2         
    plt.gcf().canvas.draw()

# Random BS
#polygon = [(0.1, 0.4), (0.3, 0.7), (0.8, 0.3), (0.9, 0.1), (0.1, 0.4), (0.6, 0.7), (0.4, 0.8)]
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
]
edges = list(zip(polygon, polygon[1:] + polygon[:1]))
plt.figure(figsize=(10, 10))
plt.gca().set_aspect("equal")
xs, ys = zip(*polygon)
output_file = r"C:\Users\mitura\Documents\Python_scripts\Polygon\Perimeter.txt"
draw_contours(edges, output_file)
plt.plot(xs, ys, "b-", linewidth=0.8)
plt.show()

def read_pairs_from_file(file_path):
    pairs = []

    with open(file_path, "r") as f:
        lines = f.readlines()
        for i in range(0, len(lines), 1):
            coordinates = lines[i].strip().split(',')
            x1, y1, x2, y2 = map(float, coordinates)
            pairs.append(((x1, y1), (x2, y2)))

    return pairs

speed_off = 200
speed_on = 2
laser_output = 2.65

input_file = r"C:\Users\mitura\Documents\Python_scripts\Polygon\Perimeter.txt"
pairs = read_pairs_from_file(input_file)

output_file = r"C:\Users\mitura\Documents\Python_scripts\Polygon\Polygon_draw.fab"
with open(output_file, "w") as fab_file:
    for pair in pairs:
        x1, y1 = pair[0]
        x2, y2 = pair[1]
        fab_file.write(f"c\t0\t{x1:.6f}\t{y1:.6f}\t0.000000\t{speed_off:.6f}\t{speed_off:.6f}\t{speed_off:.6f}\t0.000000\t0\n")
        fab_file.write(f"c\t1\t{x2:.6f}\t{y2:.6f}\t0.000000\t{speed_on:.6f}\t{speed_on:.6f}\t{speed_on:.6f}\t{laser_output:.6f}\t0\n")




