#!/usr/bin/env python3

import os
from collections import deque
import sys
import heapq  # For Dijkstra's priority queue


def solve_few(n, edges, s, t, red_vertices):
    """
    Finds the path from s to t with the *minimum* number of red vertices
    using Dijkstra's algorithm.
    """

    # --- 1. Build Adjacency List ---
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

    # --- 2. Initialize Dijkstra's ---

    # The priority queue stores: (cost, vertex)
    # "cost" is the count of red vertices on the path so far.
    pq = []

    # distances[vertex] = min cost (min red vertices) to reach that vertex
    distances = {}

    # --- 3. Set up Start Node ---
    start_cost = 1 if s in red_vertices else 0
    heapq.heappush(pq, (start_cost, s))
    distances[s] = start_cost

    # --- 4. Run Dijkstra's Algorithm ---
    while pq:
        # Get the node with the lowest cost
        current_cost, current_vertex = heapq.heappop(pq)

        # If this is the target, we're done!
        if current_vertex == t:
            return current_cost

        # If we've already found a cheaper path, skip this one
        if current_cost > distances.get(current_vertex, float('inf')):
            continue

        # --- 5. Explore Neighbors ---
        for neighbor in adj.get(current_vertex, []):

            # The *new* cost to reach the neighbor is the cost to get to us,
            # *plus* 1 if the neighbor is red.
            cost_of_neighbor_node = 1 if neighbor in red_vertices else 0
            new_cost = current_cost + cost_of_neighbor_node

            # If this is a cheaper path to the neighbor...
            if new_cost < distances.get(neighbor, float('inf')):
                distances[neighbor] = new_cost
                heapq.heappush(pq, (new_cost, neighbor))

    # --- 6. No Path Found ---
    return -1


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

        # Call the "Few" solver
        result = solve_few(n, edges, s, t, red_vertices)
        return result

    except Exception as e:
        print(
            f"Error processing file: {file_path}. Error: {e}", file=sys.stderr)
        return -1


def main():
    """
    Main function to run the "Few" problem solver.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_dir = os.path.join(script_dir, 'data')
    output_dir = os.path.join(script_dir, 'output')

    # --- Process the directory ---
    output_subdir = os.path.join(output_dir, 'few')
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
    print(f"Results for 'few' are in: {output_subdir}", file=sys.stderr)


if __name__ == "__main__":
    main()
