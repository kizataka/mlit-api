import fitz

pdf_document = fitz.open("./PORT28001010001.pdf")

page = pdf_document[0]

drawing_objects = page.get_drawings()

# count = 0
# for obj in drawing_objects:
#     print(f"Type: {obj['type']}, Details: {obj}")

# 線オブジェクトのみを抽出
lines = [obj for obj in drawing_objects if obj["type"] == 's']

# 線オブジェクトの座標を取得
line_coords = []
for line in lines:
    for item in line["items"]:
        if item[0] == "l":  # "l"は線のセグメントを表す
            start_point = (item[1].x, item[1].y)
            end_point = (item[2].x, item[2].y)
            line_coords.append((start_point, end_point))

# 線と線の交点を計算する関数
def calculate_intersection(line1, line2):
    x1, y1 = line1[0]
    x2, y2 = line1[1]
    x3, y3 = line2[0]
    x4, y4 = line2[1]

    denominator = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if denominator == 0:
        return None  # 平行線

    intersect_x = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / denominator
    intersect_y = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / denominator

    return (intersect_x, intersect_y)

# 表全体の枠の四隅の座標を求める関数
def find_bounding_box(points):
    min_x = min(point[0] for point in points)
    max_x = max(point[0] for point in points)
    min_y = min(point[1] for point in points)
    max_y = max(point[1] for point in points)
    
    return (min_x, min_y), (max_x, min_y), (min_x, max_y), (max_x, max_y)

# すべての線ペアの交点を計算
intersections = []
for i in range(len(line_coords)):
    for j in range(i + 1, len(line_coords)):
        intersection = calculate_intersection(line_coords[i], line_coords[j])
        if intersection:
            intersections.append(intersection)

# 交点の結果を表示
# for intersect in intersections:
#     print(f"Intersection: {intersect}")

print("交点の総数：", len(intersections))

# 表全体の枠の四隅の座標を計算
bottom_left, bottom_right, top_left, top_right = find_bounding_box(intersections)

# 表の四隅の座標
print("*"*20, "表の四隅の座標", "*"*20)
print(f"Top Left: {top_left}")
print(f"Top Right: {top_right}")
print(f"Bottom Left: {bottom_left}")
print(f"Bottom Right: {bottom_right}")

count = 0
x_coordinates = []
for intersect in intersections:
    if intersect[1] == top_left[1]:
        x_coordinates.append(intersect[0])
        count += 1

print(count)
x_coordinates.append(top_right[0])
x_coordinates.append(bottom_left[0])
x_coordinates = sorted(x_coordinates)
x_coordinates = [round(x_coordinate, 2) for x_coordinate in x_coordinates]
print(x_coordinates)

differences = []
for i in range(len(x_coordinates) - 1):
    difference = x_coordinates[i+1] - x_coordinates[i]
    differences.append(difference)

differences = [round(difference, 2) for difference in differences]
print(differences)