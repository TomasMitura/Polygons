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
        for i in range(0, len(intersection_points), 2):
            f.write(f"{intersection_points[i][0]}, {intersection_points[i][1]}, {intersection_points[i+1][0]}, {intersection_points[i+1][1]}\n")
              
    plt.gcf().canvas.draw()

# Random BS
polygon = random_polygon(num_points=20)
polygon.append(polygon[0])
edges = list(zip(polygon, polygon[1:] + polygon[:1]))
plt.figure(figsize=(10, 10))
plt.gca().set_aspect("equal")
xs, ys = zip(*polygon)
output_file = r"C:\Users\mitura\Documents\Python_scripts\Polygon\Perimeter.txt"
draw_contours(edges, output_file)
plt.plot(xs, ys, "b-", linewidth=0.8)
plt.show()
