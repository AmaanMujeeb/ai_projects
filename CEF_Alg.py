import trimesh
import numpy as np
import itertools

def get_continous_edge_positions(container_mesh, step_size=1.0):
    if len(container_mesh.vertices) == 0:
        return [(0, 0, 0)]

    edges = container_mesh.edges
    vertices = container_mesh.vertices
    current_points = []

    for edge in edges:
        start_point = vertices[edge[0]]
        end_point = vertices[edge[1]]

        direction = end_point - start_point
        length = np.linalg.norm(direction)

        if length > 0:
            direction_unit = direction / length
            num_steps = int(np.ceil(length / step_size)) + 1

            for step in range(num_steps):
                distance = min(length, step * step_size)
                position = start_point + distance * direction_unit
                current_points.append(tuple(position))

    return list(set(current_points))

def boxes_overlap(mesh1, mesh2):
    bounds1 = mesh1.bounds
    bounds2 = mesh2.bounds

    overlap_x = (bounds1[0][0] < bounds2[1][0]) and (bounds1[1][0] > bounds2[0][0])
    overlap_y = (bounds1[0][1] < bounds2[1][1]) and (bounds1[1][1] > bounds2[0][1])
    overlap_z = (bounds1[0][2] < bounds2[1][2]) and (bounds1[1][2] > bounds2[0][2])

    return overlap_x and overlap_y and overlap_z

def calculate_container_volume(current_boxes):
    combined = trimesh.util.concatenate(current_boxes)
    bounds = combined.bounds
    volume = (bounds[1][0]-bounds[0][0]) * (bounds[1][1]-bounds[0][1]) * (bounds[1][2]-bounds[0][2])
    return volume

def get_all_rotations(box_dims):
    rotations = []
    for perm in itertools.permutations(box_dims):
        rotations.append(list(perm))
    return rotations

def place_box(container, new_box, position):
    new_box_moved = new_box.copy()
    new_box_moved.apply_translation(position)
    if container is None:
        return new_box_moved
    if boxes_overlap(container, new_box_moved):
        return None
    return new_box_moved

def recursive_packing(remaining_boxes, current_boxes, best_result, step_size=1.0):
    if not remaining_boxes:
        current_volume = calculate_container_volume(current_boxes)
        if current_volume < best_result['volume']:
            best_result['volume'] = current_volume
            best_result['arrangement'] = [box.copy() for box in current_boxes]
        return

    current_box_dims = remaining_boxes[0]
    next_remaining = remaining_boxes[1:]

    current_container = trimesh.util.concatenate(current_boxes) if current_boxes else None

    for rotation in set(itertools.permutations(current_box_dims)):
        dims = np.array(rotation)
        box_mesh = trimesh.creation.box(
            extents=dims,
            transform=trimesh.transformations.translation_matrix(dims / 2.0)
        )
        candidate_positions = get_continous_edge_positions(current_container, step_size) if current_container else [(0, 0, 0)]
        for point in candidate_positions:
            placed_box = place_box(current_container, box_mesh, point)
            if placed_box is not None:
                new_box = current_boxes + [placed_box]
                recursive_packing(next_remaining, new_box, best_result, step_size)

def find_minimum_volume(boxes, step_size):
    boxes_sorted = sorted(boxes, key=lambda dim: dim[0] * dim[1] * dim[2])
    best_result = {
        'volume': float('inf'),
        'arrangement': []
    }
    recursive_packing(boxes_sorted, [], best_result, step_size)
    return best_result

def main():
    input_box_dims = []
    for i in range(3):
        w = int(input("Enter width: "))
        d = int(input("Enter depth: "))
        h = int(input("Enter height: "))
        input_box_dims.append([w, d, h])

    print("Your boxes: ", input_box_dims)
    print("Calculating minimum volume with CONTINUOUS edge following...")

    result = find_minimum_volume(input_box_dims, step_size = 1.0)

    print("*** RESULTS ***")
    print(f"Minimum container volume: {result['volume']:.2f}")

    if result['arrangement']:
        combined = trimesh.util.concatenate(result['arrangement'])
        bounds = combined.bounds
        print(f"Container dimensions: {bounds[1][0] - bounds[0][0]:.2f} x {bounds[1][1] - bounds[0][1]:.2f} x {bounds[1][2] - bounds[0][2]:.2f}")

if __name__ == "__main__":
    main()