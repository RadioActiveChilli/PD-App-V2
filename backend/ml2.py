import math

def calculate_angle(point1, point2, point3):
    """Calculate the angle formed by three points (point1-point2-point3)."""
    v1 = (point2[0] - point1[0], point2[1] - point1[1])
    v2 = (point3[0] - point2[0], point3[1] - point2[1])
    
    dot_product = v1[0] * v2[0] + v1[1] * v2[1]
    mag_v1 = math.sqrt(v1[0]**2 + v1[1]**2)
    mag_v2 = math.sqrt(v2[0]**2 + v2[1]**2)
    
    # Check for zero magnitude to avoid division by zero
    if mag_v1 == 0 or mag_v2 == 0:
        return 0

    cos_angle = dot_product / (mag_v1 * mag_v2)
    cos_angle = max(min(cos_angle, 1), -1)

    angle = math.acos(cos_angle)
    angle_degrees = math.degrees(angle)
    return angle_degrees

def average_angle_in_group(points, start_index, group_size):
    """Calculate the average angle in a group of consecutive points."""
    total_angle = 0
    for i in range(start_index + 1, start_index + group_size - 1):
        angle = calculate_angle(points[i - 1], points[i], points[i + 1])
        total_angle += angle
    average_angle = total_angle / (group_size - 2)
    return average_angle

def average_angle_between_groups(points, group_size=5):
    """Calculate the average angle between consecutive groups of points."""
    if len(points) < group_size:
        return 0

    group_angles = []
    for i in range(len(points) - group_size + 1):
        group_angle = average_angle_in_group(points, i, group_size)
        group_angles.append(group_angle)
    
    if not group_angles:
        return 0
    
    overall_average_angle = sum(group_angles) / len(group_angles)
    return overall_average_angle

if __name__ == "__main__":
    # Example usage
    user_drawing = [[69,16],[70,16],[71,16]]
    group_size = 3
    overall_average_angle = average_angle_between_groups(user_drawing, group_size)
    print(f"The average angle between consecutive groups of {group_size} points is {overall_average_angle:.9f} degrees.")
