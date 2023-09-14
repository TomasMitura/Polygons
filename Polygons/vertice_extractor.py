import rhinoscriptsyntax as rs

def export_polygon_points_to_txt():
    # Prompt the user to select the polygon
    polygon = rs.GetObject("Select the polygon", rs.filter.curve)

    if not polygon:
        print("No polygon selected.")
        return

    # Get the control points of the polygon
    points = rs.PolylineVertices(polygon)

    if not points:
        print("No points found.")
        return

    # Prompt the user for the file path to save the points
    file_path = rs.SaveFileName("Save points as", "Text Files (*.txt)|*.txt||")

    if not file_path:
        print("No file selected.")
        return

    # Write the points to the .txt file
    with open(file_path, "w") as file:
        for point in points:
            file.write(f"{point[0]}, {point[1]}, {point[2]}\n")

    print(f"Points saved to {file_path}")

export_polygon_points_to_txt()