import os
from collections import deque
import sys


def output_to_console(result):
    """Print result to the console."""
    print(result, file=sys.stdout)


def write_to_output_file(result, output_file):
    """Write result to a specific output file."""
    try:
        with open(output_file, 'a') as file:
            file.write(str(result) + '\n')
    except Exception as e:
        print(
            f"Error writing to output file {output_file}: {e}", file=sys.stderr)


def solve_none(n, edges, s, t, red_vertices):
    """
    Finds the length of the shortest s, t-path internally avoiding R using BFS.

    Per the problem definition:
    - "Internally avoiding R" means a path v_1, ..., v_l is valid if
      v_i is not in R for all 1 < i < l.
    - This means s (v_1) and t (v_l) ARE allowed to be red.
    """

    # --- 1. Build Adjacency List ---
    adj = {}
    for edge_line in edges:
        edge = edge_line.strip()
        # Check for both directed and undirected
        if ' -- ' in edge:
            u, v = edge.split(' -- ')
            adj.setdefault(u, []).append(v)
            adj.setdefault(v, []).append(u)
        elif ' -> ' in edge:
            u, v = edge.split(' -> ')
            adj.setdefault(u, []).append(v)
            # For directed, we don't add the reverse edge

    # --- 2. Handle Edge Cases ---
    if s == t:
        return 0

    # --- 3. Initialize BFS ---
    queue = deque([(s, 0)])  # (vertex, distance)
    visited = {s}

    # --- 4. Run BFS ---
    while queue:
        current_vertex, dist = queue.popleft()

        for neighbor in adj.get(current_vertex, []):

            if neighbor in visited:
                continue

            # CASE 1: The neighbor is the target 't'.
            # This is always a valid path.
            if neighbor == t:
                return dist + 1

            # CASE 2: The neighbor is NOT 't' and IS RED.
            # This is an "internal" node. We are not allowed
            # to use this path. Skip this neighbor.
            if neighbor in red_vertices:
                continue

            # CASE 3: The neighbor is NOT 't' and is NOT RED.
            # This is a valid internal node. Add it to the queue.
            visited.add(neighbor)
            queue.append((neighbor, dist + 1))

    # --- 5. No Path Found ---
    return -1


def process_file(file_path):
    """
    Reads and processes each file based on the *new* format.
    """
    try:
        with open(file_path, 'r') as file:
            data = [line.strip() for line in file.readlines()
                    if line.strip()]  # Read all non-empty lines
    except Exception as e:
        print(
            f"Unable to read test case file: {file_path}. Error: {e}", file=sys.stderr)
        return -1

    try:
        # --- 1. Read Counts (Line 0) ---
        n, m, r = map(int, data[0].split())

        # --- 2. Read s and t (Line 1) ---
        s, t = data[1].split()

        # --- 3. Read Vertices and Red Vertices (Lines 2 to n+1) ---
        vertex_lines_start = 2
        vertex_lines_end = 2 + n
        vertex_lines = data[vertex_lines_start: vertex_lines_end]

        red_vertices = set()
        for line in vertex_lines:
            if line.endswith('*'):
                # Get vertex name, remove the " *"
                vertex_name = line[:-1].strip()
                red_vertices.add(vertex_name)

        # --- 4. Read Edges (Lines n+2 to n+m+1) ---
        edge_start_index = vertex_lines_end
        edge_end_index = edge_start_index + m
        edges = data[edge_start_index: edge_end_index]

        # --- 5. Validate File ---
        # Check if we have the right number of red vertices
        if len(red_vertices) != r:
            print(
                f"Warning: File {file_path} said r={r} but found {len(red_vertices)} red vertices.", file=sys.stderr)

        # Check if we have the right number of edges
        if len(edges) != m:
            print(
                f"Warning: File {file_path} said m={m} but found {len(edges)} edges.", file=sys.stderr)

        # --- 6. Call the Solver ---
        shortest_path = solve_none(n, edges, s, t, red_vertices)
        return shortest_path

    except Exception as e:
        print(
            f"Unable to process test case file: {file_path}. Error: {e}", file=sys.stderr)
        return -1


def process_directory(input_dir, output_dir):
    """Process all files in the input directory and write the results."""
    output_subdir = os.path.join(output_dir, 'none')
    if not os.path.exists(output_subdir):
        try:
            os.makedirs(output_subdir)
        except OSError as e:
            print(
                f"Could not create output directory: {output_subdir}. Error: {e}", file=sys.stderr)
            return

    try:
        files = os.listdir(input_dir)
    except FileNotFoundError:
        print(f"Input directory not found: {input_dir}", file=sys.stderr)
        return
    except NotADirectoryError:
        print(f"Input path is not a directory: {input_dir}", file=sys.stderr)
        return

    for file_name in sorted(files):
        file_path = os.path.join(input_dir, file_name)

        if os.path.isfile(file_path):
            print(f"--- Processing {file_name} ---", file=sys.stderr)

            result = process_file(file_path)

            output_to_console(result)

            output_file = os.path.join(output_subdir, file_name)
            write_to_output_file(result, output_file)


def main():

    # Set your input directory (where the test case files are)
    input_dir = r'E:\Study ITU\Seminars in Data Science\algorithm design\data'

    # Set your output directory (where results will be written)
    output_dir = r'E:\Study ITU\Seminars in Data Science\algorithm design\output'

    # Process the directory and handle all test cases
    process_directory(input_dir, output_dir)

    print("\nProcessing complete.", file=sys.stderr)
    print(
        f"Results for 'none' are in: {os.path.join(output_dir, 'none')}", file=sys.stderr)


if __name__ == "__main__":
    main()
