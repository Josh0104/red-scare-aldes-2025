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


def alternate_solution(n, edges, s, t, red_vertices):
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
    '''
    If there are no red vertices, then every path
    is invalid.
    '''
    if len(red_vertices) == 0:
        return False
    '''If s and t are the same, is there a valid path?
    It isn't technically breaking the alternate rule,
    but it isn't fulfilling it either.
    '''
    if s == t:
        return False


    # --- 3. Initialize BFS ---
    # True = red, False = black
    temp_color = None
    if s in red_vertices:
        temp_color = True
    else:
        temp_color = False

    queue = deque([(s, temp_color)])  # (vertex, color)
    visited = {s}

    # --- 4. Run BFS ---
    while queue:
        current_vertex, color = queue.popleft()

        for neighbor in adj.get(current_vertex, []):

            if neighbor in visited:
                continue

            if color:  # if current vertex is red
                if neighbor in red_vertices: # neighbor vertex is also red
                    continue
                else:  # if neighbor vertex is black
                    visited.add(neighbor)
                    queue.append((neighbor, False))
            else:  # if current vertex is black
                if neighbor in red_vertices: # neighbor vertex is red
                    visited.add(neighbor)
                    queue.append((neighbor, True))
                else:  # if neighbor vertex is also black
                    continue

            if neighbor == t:
                return True


    # --- 5. No Path Found ---
    return False


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
        alternate_path = alternate_solution(n, edges, s, t, red_vertices)
        return alternate_path

    except Exception as e:
        print(
            f"Unable to process test case file: {file_path}. Error: {e}", file=sys.stderr)
        return -1


def process_directory(input_dir, output_dir):
    """Process all files in the input directory and write the results."""
    output_subdir = os.path.join(output_dir, 'alternate')
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

        # Ignore README or non-txt files
        if not file_name.lower().endswith('.txt'):
            continue

        if os.path.isfile(file_path):
            print(f"--- Processing {file_name} ---", file=sys.stderr)

            result = process_file(file_path)

            output_to_console(result)

            output_file = os.path.join(output_subdir, file_name)
            write_to_output_file(result, output_file)


def main():
    # Relative paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_dir = os.path.join(script_dir, 'data')
    output_dir = os.path.join(script_dir, 'output')

    # process_directory expects string paths
    process_directory(input_dir, output_dir)

    print("\nProcessing complete.", file=sys.stderr)
    print(f"Results for 'alternate' are in: {os.path.join(output_dir, 'alternate')}", file=sys.stderr)


if __name__ == "__main__":
    main()
