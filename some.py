import os
from collections import deque
import sys

# --- HELPER FUNCTION: Build Adjacency List ---


def _build_adjacency_list(edges):
    """
    Builds a standard forward adjacency list.
    """
    adj = {}
    for edge_line in edges:
        edge = edge_line.strip()

        if ' -- ' in edge:
            u, v = edge.split(' -- ')
            adj.setdefault(u, []).append(v)
            adj.setdefault(v, []).append(u)

        elif ' -> ' in edge:
            u, v = edge.split(' -> ')
            adj.setdefault(u, []).append(v)

    return adj

# --- HELPER FUNCTION: Simple Reachability BFS ---


def _bfs_can_reach(start_node, end_node, adj):

    if start_node == end_node:
        return True

    queue = deque([start_node])
    visited = {start_node}

    # Check if start_node is even in the graph
    if start_node not in adj:
        return False

    while queue:
        current_vertex = queue.popleft()

        for neighbor in adj.get(current_vertex, []):
            if neighbor == end_node:
                return True

            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    return False

# --- "SOME" PROBLEM SOLVER ---


def solve_some(n, edges, s, t, red_vertices):

    # --- 1. Build forward graph ---
    adj = _build_adjacency_list(edges)

    # --- 2. Loop through every red vertex ---
    for r in red_vertices:

        # --- 3. Run two BFSs ---
        # Check Part 1: Can s reach r?
        can_s_reach_r = _bfs_can_reach(s, r, adj)

        # Check Part 2: Can r reach t?
        # We only run this if Part 1 was successful, to save time.
        if can_s_reach_r:
            can_r_reach_t = _bfs_can_reach(r, t, adj)

            # If both parts are true, we found a valid path
            if can_r_reach_t:
                return "true"  # Found a valid path

    # If we check all red vertices and find no such path
    return "false"


def process_file(file_path):
    """
    Reads a file, parses it, and calls the solver.
    """
    try:
        with open(file_path, 'r') as file:
            data = [line.strip() for line in file.readlines() if line.strip()]
    except Exception as e:
        print(f"Unable to read file: {file_path}. Error: {e}", file=sys.stderr)
        return -1

    try:
        n, m, r = map(int, data[0].split())
        s, t = data[1].split()

        vertex_lines_start = 2
        vertex_lines_end = 2 + n
        vertex_lines = data[vertex_lines_start: vertex_lines_end]

        red_vertices = set()
        for line in vertex_lines:
            if line.endswith('*'):
                red_vertices.add(line[:-1].strip())

        edge_start_index = vertex_lines_end
        edge_end_index = edge_start_index + m
        edges = data[edge_start_index: edge_end_index]

        # Call the "Some" solver
        result = solve_some(n, edges, s, t, red_vertices)
        return result

    except Exception as e:
        print(
            f"Error processing file: {file_path}. Error: {e}", file=sys.stderr)
        return -1


def main():
    """
    Main function to run the "Some" problem solver.
    """

    input_dir = r'E:\Study ITU\Seminars in Data Science\algorithm design\data'
    output_dir = r'E:\Study ITU\Seminars in Data Science\algorithm design\output'

    # --- Process the directory ---
    output_subdir = os.path.join(output_dir, 'some')
    if not os.path.exists(output_subdir):
        os.makedirs(output_subdir)

    try:
        files = os.listdir(input_dir)
    except Exception as e:
        print(f"Error reading input directory: {e}", file=sys.stderr)
        return

    for file_name in sorted(files):
        file_path = os.path.join(input_dir, file_name)

        if os.path.isfile(file_path):
            print(f"--- Processing {file_name} ---", file=sys.stderr)

            # 1. Process the file
            result = process_file(file_path)

            # 2. Output to console
            print(result, file=sys.stdout)

            # 3. Write to output file
            output_file = os.path.join(output_subdir, file_name)
            try:
                with open(output_file, 'a') as f:
                    f.write(str(result) + '\n')
            except Exception as e:
                print(f"Error writing to output file: {e}", file=sys.stderr)

    print("\nProcessing complete.", file=sys.stderr)
    print(f"Results for 'some' are in: {output_subdir}", file=sys.stderr)


if __name__ == "__main__":
    main()
