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


def _build_adjacency_lists(edges):
    """
    Builds both forward and reverse adjacency lists from the edge data.
    """
    adj = {}
    adj_reversed = {}

    for edge_line in edges:
        edge = edge_line.strip()

        if ' -- ' in edge:
            u, v = edge.split(' -- ')
            # Undirected: add edge in both directions for both graphs
            adj.setdefault(u, []).append(v)
            adj.setdefault(v, []).append(u)
            adj_reversed.setdefault(u, []).append(v)
            adj_reversed.setdefault(v, []).append(u)

        elif ' -> ' in edge:
            u, v = edge.split(' -> ')
            # Directed: add forward edge to adj
            adj.setdefault(u, []).append(v)
            # Add reverse edge to adj_reversed
            adj_reversed.setdefault(v, []).append(u)

    return adj, adj_reversed


def _bfs_get_reachable(start_node, adj_list):

    queue = deque([start_node])
    visited = {start_node}

    # Check if start_node is even in the graph
    if start_node not in adj_list:
        # Still return {start_node} because a node can reach itself
        return visited

    while queue:
        current_vertex = queue.popleft()
        for neighbor in adj_list.get(current_vertex, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    return visited

# --- "SOME" PROBLEM SOLVER ---


def solve_some(n, edges, s, t, red_vertices):

    # --- 1. Build forward and reverse graphs ---
    adj, adj_reversed = _build_adjacency_lists(edges)

    # Find all vertices that s can reach
    reachable_from_s = _bfs_get_reachable(s, adj)

    # Find all vertices that can reach t
    can_reach_t = _bfs_get_reachable(t, adj_reversed)

    # --- 4. Check for overlap ---
    # We just need to find one red vertex 'r' that is in *both* sets
    for r in red_vertices:
        if r in reachable_from_s and r in can_reach_t:
            return "true"  # *** CORRECTED ***

    # If we check all red vertices and find no such path
    return "false"


def process_file(file_path):

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
        if len(red_vertices) != r:
            print(
                f"Warning: File {file_path} said r={r} but found {len(red_vertices)} red vertices.", file=sys.stderr)
        if len(edges) != m:
            print(
                f"Warning: File {file_path} said m={m} but found {len(edges)} edges.", file=sys.stderr)

        # --- 6. Call the Solver ---
        result = solve_some(n, edges, s, t, red_vertices)
        return result

    except Exception as e:
        print(
            f"Unable to process test case file: {file_path}. Error: {e}", file=sys.stderr)
        return -1


def process_directory(input_dir, output_dir):
    """Process all files in the input directory and write the results."""

    output_subdir = os.path.join(output_dir, 'some')
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
        f"Results for 'some' are in: {os.path.join(output_dir, 'some')}", file=sys.stderr)


if __name__ == "__main__":
    main()
