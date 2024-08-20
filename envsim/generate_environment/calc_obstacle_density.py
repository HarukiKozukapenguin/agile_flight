import csv
import math
import yaml

# Path to the CSV file
csv_file = '/home/hal/agile_flight/flightmare/flightpy/configs/vision/real_tree_random_13/environment_500/static_obstacles.csv'

# Path to the YAML file
yaml_file = '/home/hal/agile_flight/flightmare/flightpy/configs/vision/real_tree_random_13/environment_500/dynamic_obstacles.yaml'

# Range for obstacle existence
x_min, x_max = 0, 60
y_min, y_max = -10, 10

# body_radius
body_radius = 0.25

# Total obstacle area within the valid range
total_obstacle_area = 0.0
total_obstacle_count = 0

# Read the CSV file
with open(csv_file, newline='') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        x = float(row[1])
        y = float(row[2])
        radius = float(row[7])

        # Add body_radius to the obstacle's radius
        effective_radius = radius + body_radius

        # Check if the obstacle is within the specified range
        if x_min <= x <= x_max and y_min <= y <= y_max:
            # Calculate the area of the circle and add it
            obstacle_area = math.pi * effective_radius ** 2
            total_obstacle_area += obstacle_area
            total_obstacle_count += 1

# Read the YAML file
with open(yaml_file, 'r') as yamlfile:
    data = yaml.safe_load(yamlfile)

    # Process each object in the YAML file
    for key, obj in data.items():
        if isinstance(obj, dict) and 'position' in obj and 'scale' in obj:
            x = float(obj['position'][0])
            y = float(obj['position'][1])
            radius = float(obj['scale'][0])  # scale is treated as the radius
            
            # Add body_radius to the obstacle's radius
            effective_radius = radius + body_radius

            # Check if the obstacle is within the specified range
            if x_min <= x <= x_max and y_min <= y <= y_max:
                # Calculate the area of the circle and add it
                obstacle_area = math.pi * effective_radius ** 2
                total_obstacle_area += obstacle_area
                total_obstacle_count += 1

# Calculate the area of the range
area_range = (x_max - x_min) * (y_max - y_min)

# Calculate the obstacle density
obstacle_density = total_obstacle_area / area_range
obstacle_count_ratio = total_obstacle_count / area_range

# Print the result
print(f'Obstacle Density: {obstacle_density}')
print(f'Number of Obstacles / Total Area: {obstacle_count_ratio}')
