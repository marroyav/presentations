#!/usr/bin/env python3

from __future__ import annotations

import argparse
import csv
import json
import shutil
import subprocess
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
VIEWS_PATH = ROOT / "views" / "views.json"
OUTPUT_DIR = ROOT / "output"


LAYER_COLORS = {
    "repository": "#F6F6F6",
    "control": "#DCEBFA",
    "analog": "#DFF0DF",
    "frontend": "#E8F4E2",
    "timing": "#FCE7D3",
    "trigger": "#F8DCDD",
    "transport": "#E9E0D8",
    "debug": "#D9F0F0",
    "verification": "#E9E3F6",
    "build": "#E7E7E7",
    "clock": "#FFF7D6",
    "contract": "#F7F1D8",
}

GROUP_COLORS = {
    "repository": "#F3F3F3",
    "control": "#EDF5FD",
    "analog": "#EFF8EF",
    "frontend": "#F2FAEE",
    "timing": "#FFF1E4",
    "trigger": "#FCEBEC",
    "transport": "#F3ECE8",
    "debug": "#EEF9F9",
    "verification": "#F3EEF9",
    "build": "#F2F2F2",
    "clock": "#FFF9E7",
    "contracts": "#FBF7E7",
}

RELATION_STYLES = {
    "contains": {"color": "#7A7A7A", "style": "solid", "penwidth": "1.6"},
    "configures": {"color": "#4E79A7", "style": "dashed", "penwidth": "1.8"},
    "readiness_prereq": {"color": "#F28E2B", "style": "dashed", "penwidth": "1.8"},
    "streams_to": {"color": "#444444", "style": "solid", "penwidth": "1.9"},
    "observes": {"color": "#76B7B2", "style": "dotted", "penwidth": "1.7"},
    "clock_source": {"color": "#59A14F", "style": "solid", "penwidth": "1.9"},
    "clocks": {"color": "#59A14F", "style": "solid", "penwidth": "2.0"},
    "qualifies": {"color": "#8CD17D", "style": "dashed", "penwidth": "1.7"},
    "drives": {"color": "#9C755F", "style": "dashed", "penwidth": "1.7"},
    "asserts": {"color": "#B6992D", "style": "dashed", "penwidth": "1.8"},
    "enables": {"color": "#B07AA1", "style": "dashed", "penwidth": "1.8"},
    "produces": {"color": "#9C755F", "style": "solid", "penwidth": "1.9"},
}

RELATION_ABBREVIATIONS = {
    "configures": "cfg",
    "readiness_prereq": "rdy",
    "asserts": "ast",
    "enables": "enb",
    "streams_to": "str",
    "observes": "obs",
    "qualifies": "qlf",
    "drives": "drv",
    "produces": "prd",
}


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def load_views() -> dict[str, dict]:
    with VIEWS_PATH.open(encoding="utf-8") as handle:
        return json.load(handle)["views"]


def quote(value: str) -> str:
    return '"' + value.replace('"', r"\"") + '"'


def node_style(node: dict[str, str]) -> dict[str, str]:
    fill = LAYER_COLORS.get(node["layer"], "#FFFFFF")
    style = "rounded,filled"
    penwidth = "1.7"
    color = "#5A5A5A"
    shape = "box"

    if node["kind"] == "repo":
        shape = "folder"
        penwidth = "2.0"
    elif node["kind"] == "clock_source":
        shape = "ellipse"
    elif node["kind"] == "build":
        shape = "component"
    elif node["layer"] == "contract":
        shape = "hexagon"
        penwidth = "1.8"

    if node["ownership"] == "imported":
        style += ",dashed"
    elif node["ownership"] == "platform":
        style += ",bold"

    return {
        "shape": shape,
        "style": style,
        "fillcolor": fill,
        "color": color,
        "penwidth": penwidth,
        "fontname": "Helvetica",
        "fontsize": "12",
        "margin": "0.16,0.10",
        "label": node["label"],
    }


def merge_attrs(base: dict[str, str], override: dict[str, str] | None) -> dict[str, str]:
    merged = base.copy()
    if override:
        merged.update({key: str(value) for key, value in override.items()})
    return merged


def edge_style(edge: dict[str, str], view: dict) -> dict[str, str]:
    base = RELATION_STYLES[edge["relation"]].copy()
    base["fontname"] = "Helvetica"
    base["fontsize"] = "10.5"
    base["arrowsize"] = "0.9"
    show_edge_labels = view.get("show_edge_labels", False)
    label_mode = view.get("label_mode", "smart")
    hidden_relations = set(view.get("hide_edge_labels_for_relations", []))
    if show_edge_labels and edge["relation"] not in hidden_relations:
        label = edge["label"].strip()
        condition = edge["condition"].strip()
        if label_mode == "label":
            if label:
                base["label"] = label
        elif label_mode == "condition":
            if condition:
                base["label"] = condition
        elif label_mode == "both":
            if label:
                base["label"] = label
            if condition:
                base["xlabel"] = condition
                base["fontcolor"] = base["color"]
        elif label_mode == "smart":
            if label and condition and label == condition:
                base["label"] = label
            else:
                if label:
                    base["label"] = label
                if condition:
                    base["xlabel"] = condition
                    base["fontcolor"] = base["color"]
    return base


def emit_attrs(attrs: dict[str, str]) -> str:
    return ", ".join(f"{key}={quote(value)}" for key, value in attrs.items())


def ordered_nodes(node_ids: list[str], nodes_by_id: dict[str, dict[str, str]]) -> list[dict[str, str]]:
    return [nodes_by_id[node_id] for node_id in node_ids if node_id in nodes_by_id]


def render_dot(view_name: str, view: dict, nodes_by_id: dict[str, dict[str, str]], edges: list[dict[str, str]]) -> str:
    node_ids = set(view["node_ids"])
    excluded_edges = {tuple(item) for item in view.get("exclude_edges", [])}
    selected_edges = [
        edge
        for edge in edges
        if edge["relation"] in view["relations"]
        and edge["src"] in node_ids
        and edge["dst"] in node_ids
        and (edge["src"], edge["dst"]) not in excluded_edges
    ]
    selected_nodes = ordered_nodes(view["node_ids"], nodes_by_id)

    groups: dict[str, list[dict[str, str]]] = defaultdict(list)
    cluster_by = view.get("cluster_by")
    if cluster_by:
        for node in selected_nodes:
            groups[node[cluster_by]].append(node)

    graph_attrs = {
        "bgcolor": "white",
        "pad": "0.15",
        "nodesep": "0.45",
        "ranksep": "0.75",
        "splines": "spline",
        "overlap": "false",
        "rankdir": view["rankdir"],
        "fontname": "Helvetica",
        "fontsize": "16",
        "labelloc": "t",
        "labeljust": "l",
    }
    if view.get("render_title", False):
        graph_attrs["label"] = view["title"]
    graph_attrs.update({key: str(value) for key, value in view.get("graph_attrs", {}).items()})
    lines = [
        f'digraph "{view_name}" {{',
        f'  graph [{emit_attrs(graph_attrs)}];',
        '  node [fontname="Helvetica"];',
        '  edge [fontname="Helvetica"];',
    ]

    node_overrides = view.get("node_overrides", {})
    if cluster_by:
        group_order = view.get("group_order", [])
        ordered_group_names = list(group_order) + [name for name in groups if name not in group_order]
        for group_name in ordered_group_names:
            if group_name not in groups:
                continue
            group_nodes = groups[group_name]
            cluster_color = GROUP_COLORS.get(group_name, "#F6F6F6")
            cluster_id = f"cluster_{group_name}"
            lines.append(f"  subgraph {cluster_id} {{")
            lines.append(f'    graph [label={quote(group_name.replace("_", " ").title())}, bgcolor={quote(cluster_color)}, color="#D0D0D0", style="rounded"];')
            for node in group_nodes:
                attrs = merge_attrs(node_style(node), node_overrides.get(node["id"]))
                lines.append(f'    {node["id"]} [{emit_attrs(attrs)}];')
            lines.append("  }")
    else:
        for node in selected_nodes:
            attrs = merge_attrs(node_style(node), node_overrides.get(node["id"]))
            lines.append(f'  {node["id"]} [{emit_attrs(attrs)}];')

    for edge in selected_edges:
        lines.append(f'  {edge["src"]} -> {edge["dst"]} [{emit_attrs(edge_style(edge, view))}];')

    for rank_group in view.get("ranks", []):
        valid_ids = [node_id for node_id in rank_group if node_id in node_ids]
        if valid_ids:
            lines.append("  { rank=same; " + "; ".join(valid_ids) + "; }")

    lines.append("}")
    return "\n".join(lines) + "\n"


def render_graphviz(dot_path: Path) -> None:
    stem = dot_path.with_suffix("")
    for fmt in ("svg", "pdf", "png"):
        subprocess.run(
            ["dot", f"-T{fmt}", str(dot_path), "-o", str(stem.with_suffix(f".{fmt}"))],
            check=True,
        )
    pdfcrop = shutil.which("pdfcrop")
    if pdfcrop:
        pdf_path = stem.with_suffix(".pdf")
        cropped_path = stem.with_name(stem.name + "_cropped").with_suffix(".pdf")
        subprocess.run([pdfcrop, str(pdf_path), str(cropped_path)], check=True)


def dependency_edges_for_matrix(edges: list[dict[str, str]], view: dict) -> list[dict[str, str]]:
    excluded_edges = {tuple(item) for item in view.get("exclude_edges", [])}
    return [
        edge
        for edge in edges
        if edge["relation"] in view["relations"]
        and edge["relation"] in RELATION_ABBREVIATIONS
        and edge["src"] in set(view["node_ids"])
        and edge["dst"] in set(view["node_ids"])
        and (edge["src"], edge["dst"]) not in excluded_edges
    ]


def write_dependency_matrix(view: dict, nodes_by_id: dict[str, dict[str, str]], edges: list[dict[str, str]]) -> None:
    matrix_nodes = ordered_nodes(view["node_ids"], nodes_by_id)
    matrix_edges = dependency_edges_for_matrix(edges, view)
    cell_map: dict[tuple[str, str], list[str]] = defaultdict(list)
    for edge in matrix_edges:
        cell_map[(edge["src"], edge["dst"])].append(RELATION_ABBREVIATIONS[edge["relation"]])

    csv_path = OUTPUT_DIR / "dependency_matrix.csv"
    md_path = OUTPUT_DIR / "dependency_matrix.md"

    header = ["source \\ target"] + [node["label"] for node in matrix_nodes]
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(header)
        for src_node in matrix_nodes:
            row = [src_node["label"]]
            for dst_node in matrix_nodes:
                values = sorted(set(cell_map.get((src_node["id"], dst_node["id"]), [])))
                row.append("/".join(values))
            writer.writerow(row)

    with md_path.open("w", encoding="utf-8") as handle:
        handle.write("# Dependency Matrix\n\n")
        handle.write("Abbreviations: `cfg` configure, `rdy` readiness prerequisite, `ast` assert state, `enb` enable state, `qlf` qualify/gate, `str` stream, `obs` observe, `drv` build-drive, `prd` produce.\n\n")
        handle.write("| source \\\\ target | " + " | ".join(node["label"] for node in matrix_nodes) + " |\n")
        handle.write("|" + "---|" * (len(matrix_nodes) + 1) + "\n")
        for src_node in matrix_nodes:
            row = [src_node["label"]]
            for dst_node in matrix_nodes:
                values = sorted(set(cell_map.get((src_node["id"], dst_node["id"]), [])))
                row.append("/".join(values))
            handle.write("| " + " | ".join(row) + " |\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="Render reusable architecture diagrams and dependency matrix.")
    parser.add_argument("--view", help="Render only one named view.")
    args = parser.parse_args()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    nodes = load_csv(DATA_DIR / "nodes.csv")
    edges = load_csv(DATA_DIR / "edges.csv")
    views = load_views()
    nodes_by_id = {node["id"]: node for node in nodes}

    requested_views = [args.view] if args.view else list(views.keys())
    for view_name in requested_views:
        if view_name not in views:
            raise SystemExit(f"unknown view: {view_name}")
        dot_text = render_dot(view_name, views[view_name], nodes_by_id, edges)
        dot_path = OUTPUT_DIR / f"{view_name}.dot"
        dot_path.write_text(dot_text, encoding="utf-8")
        render_graphviz(dot_path)

    dependency_view = views["readiness_contracts"]
    write_dependency_matrix(dependency_view, nodes_by_id, edges)


if __name__ == "__main__":
    main()
