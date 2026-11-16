from itertools import product
from pathlib import Path

import networkx as nx
from networkx.drawing.nx_pydot import write_dot


def graph(labels, transitions):
    result = nx.DiGraph()
    for node, label in labels.items():
        result.add_node(node, label=f'"{label}"')
    for start, end, condition in transitions:
        if condition:
            result.add_edge(start, end, label=condition)
        else:
            result.add_edge(start, end)
    result.nodes["start"]["shape"] = "oval"
    result.nodes["end"]["shape"] = "oval"
    for node in result:
        if result.out_degree(node) == 2:
            result.nodes[node]["shape"] = "diamond"
    return result


AUTH = graph(
    {
        "start": "Entry", "u": "Missing username?", "p": "Missing password?",
        "m": "Missing credentials", "found": "Username in db?",
        "nf": "User not found", "load": "Read attempts",
        "locked": "Attempts >= 3?", "al": "Account locked",
        "password": "Password matches?", "inc": "Increment attempts",
        "iv": "Invalid password", "reset": "Reset attempts",
        "ok": "Authenticated", "end": "Exit",
    },
    [
        ("start", "u", ""), ("u", "m", "yes"), ("u", "p", "no"),
        ("p", "m", "yes"), ("p", "found", "no"), ("m", "end", ""),
        ("found", "nf", "no"), ("found", "load", "yes"), ("nf", "end", ""),
        ("load", "locked", ""), ("locked", "al", "yes"), ("al", "end", ""),
        ("locked", "password", "no"), ("password", "reset", "yes"),
        ("password", "inc", "no"), ("inc", "iv", ""), ("iv", "end", ""),
        ("reset", "ok", ""), ("ok", "end", ""),
    ],
)

DATA = graph(
    {
        "start": "Entry", "init": "total = 0", "i": "Next i?",
        "negative": "data[i] < 0?", "j": "Next j?", "even": "j is even?",
        "add": "total += j", "ret": "Return total", "end": "Exit",
    },
    [
        ("start", "init", ""), ("init", "i", ""), ("i", "negative", "yes"),
        ("i", "ret", "no"), ("negative", "i", "yes"), ("negative", "j", "no"),
        ("j", "even", "yes"), ("j", "i", "no"), ("even", "add", "yes"),
        ("even", "j", "no"), ("add", "j", ""), ("ret", "end", ""),
    ],
)

MATRIX = graph(
    {
        "start": "Entry", "init": "count = 0", "i": "Next row i?",
        "j": "Next element j?", "positive": "matrix[i][j] > 0?",
        "k": "Next k?", "add": "count += k % 3", "ret": "Return count",
        "end": "Exit",
    },
    [
        ("start", "init", ""), ("init", "i", ""), ("i", "j", "yes"),
        ("i", "ret", "no"), ("j", "positive", "yes"), ("j", "i", "no"),
        ("positive", "k", "yes"), ("positive", "j", "no"),
        ("k", "add", "yes"), ("k", "j", "no"), ("add", "k", ""),
        ("ret", "end", ""),
    ],
)

STATUS = graph(
    {
        "start": "Entry", "map": "Define transitions", "same": "Same status?",
        "unchanged": "No change", "transition": "Allowed transition?",
        "invalid": "Invalid transition", "role": "Non-privileged role?",
        "closed": "New status closed?", "denied": "Permission denied",
        "assign": "Assign new status", "updated": "Updated", "end": "Exit",
    },
    [
        ("start", "map", ""), ("map", "same", ""), ("same", "unchanged", "yes"),
        ("unchanged", "end", ""), ("same", "transition", "no"),
        ("transition", "invalid", "no"), ("invalid", "end", ""),
        ("transition", "role", "yes"), ("role", "closed", "yes"),
        ("role", "assign", "no"), ("closed", "denied", "yes"),
        ("closed", "assign", "no"), ("denied", "end", ""),
        ("assign", "updated", ""), ("updated", "end", ""),
    ],
)


def main():
    output = Path(__file__).resolve().parent
    lines = []
    for name, cfg in (
        ("cfg", AUTH), ("cfg_data", DATA), ("cfg_matrix", MATRIX), ("cfg_status", STATUS)
    ):
        write_dot(cfg, output / f"{name}.dot")
        nodes = cfg.number_of_nodes()
        edges = cfg.number_of_edges()
        lines.append(f"{name}: N={nodes}; E={edges}; M={edges - nodes + 2}")

    lines.append("\nAuthenticate: feasible complete routes")
    for n, path in enumerate(nx.all_simple_paths(AUTH, "start", "end"), 1):
        lines.append(f"P{n}: {' -> '.join(path)}")

    lines.append("\ncheck_access: A B C | decision")
    for a, b, c in product((0, 1), repeat=3):
        lines.append(f"{a} {b} {c} | {int((a and b) or c)}")
    lines.append("\nvalidate_input: D U | decision after the first two checks")
    for d, u in product((0, 1), repeat=2):
        lines.append(f"{d} {u} | {int(d and u)}")
    lines.append("\nauthenticate_user: U P | missing credentials")
    for u, p in product((0, 1), repeat=2):
        lines.append(f"{u} {p} | {int(u or p)}")

    (output / "cfg_analysis.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
