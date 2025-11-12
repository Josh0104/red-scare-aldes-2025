import argparse
import os
import sys

import alternate
import working_none


def read_instance(path):
    try:
        with open(path, "r", encoding="utf-8") as handle:
            lines = [line.strip() for line in handle if line.strip()]
    except OSError as error:
        print(f"Could not read {path}: {error}", file=sys.stderr)
        return None

    if len(lines) < 2:
        print(f"File {path} is too short to parse.", file=sys.stderr)
        return None

    try:
        n_str, m_str, r_str = lines[0].split()
        n = int(n_str)
        m = int(m_str)
        r = int(r_str)
        s, t = lines[1].split()
    except ValueError as error:
        print(f"Header parse failed for {path}: {error}", file=sys.stderr)
        return None

    vertex_lines = lines[2: 2 + n]
    red_vertices = set()
    for line in vertex_lines:
        if line.endswith("*"):
            red_vertices.add(line[:-1].strip())

    if len(red_vertices) != r:
        print(
            f"Warning: {path} declares {r} red vertices but found {len(red_vertices)}.",
            file=sys.stderr,
        )

    edge_lines = lines[2 + n: 2 + n + m]
    if len(edge_lines) != m:
        print(
            f"Warning: {path} declares {m} edges but found {len(edge_lines)}.",
            file=sys.stderr,
        )

    return {
        "name": os.path.basename(path),
        "n": n,
        "s": s,
        "t": t,
        "red": red_vertices,
        "edges": edge_lines,
    }


def solve_alternate(instance):
    try:
        result = alternate.alternate_solution(
            instance["n"],
            instance["edges"],
            instance["s"],
            instance["t"],
            instance["red"],
        )
    except Exception as error:
        print(f"Alternate solver failed on {instance['name']}: {error}", file=sys.stderr)
        return "?"
    return "true" if result else "false"


def solve_none(instance):
    try:
        result = working_none.solve_none(
            instance["n"],
            instance["edges"],
            instance["s"],
            instance["t"],
            instance["red"],
        )
    except Exception as error:
        print(f"None solver failed on {instance['name']}: {error}", file=sys.stderr)
        return "?"
    return str(result)


def gather_rows(data_dir):
    rows = []
    for file_name in sorted(os.listdir(data_dir)):
        if not file_name.lower().endswith(".txt"):
            continue

        file_path = os.path.join(data_dir, file_name)
        if not os.path.isfile(file_path):
            continue

        instance = read_instance(file_path)
        if instance is None:
            continue

        alt_answer = solve_alternate(instance)
        none_answer = solve_none(instance)

        row = "\t".join(
            [
                instance["name"],
                str(instance["n"]),
                alt_answer,
                "?",
                "?",
                none_answer,
                "?",
            ]
        )
        rows.append(row)
    return rows


def write_results(rows, output_path):
    header = "\t".join(["instance", "n", "A", "F", "M", "N", "S"])
    try:
        with open(output_path, "w", encoding="utf-8") as handle:
            handle.write(header + "\n")
            for row in rows:
                handle.write(row + "\n")
    except OSError as error:
        print(f"Could not write {output_path}: {error}", file=sys.stderr)
        sys.exit(1)


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    default_dir = os.path.join(script_dir, "data")
    default_output = os.path.join(script_dir, "results.txt")

    parser = argparse.ArgumentParser(description="Generate results.txt for the Red Scare assignment.")
    parser.add_argument("--data-dir", default=default_dir, help="Folder with instance files (default: %(default)s)")
    parser.add_argument("--output", default=default_output, help="Where to write the table (default: %(default)s)")
    args = parser.parse_args()

    if not os.path.isdir(args.data_dir):
        print(f"Data directory not found: {args.data_dir}", file=sys.stderr)
        sys.exit(1)

    rows = gather_rows(args.data_dir)
    write_results(rows, args.output)
    print(f"Wrote results to {args.output}")


if __name__ == "__main__":
    main()
