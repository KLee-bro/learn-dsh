#!/usr/bin/env python3
"""learn_graph.py — persistent knowledge graph for the learn-dsh plugin.

Store: propositions (claims) and chains (premises that jointly imply a
conclusion), plain JSON at ~/.dsh/learn/graph.json (override with --data-dir).
Standard library only; no network.

Usage:
  learn_graph.py [--data-dir DIR] [--format json|text] <command> [args]

Commands:
  stats
  propositions [--session ID]
  chains [--node ID]
  find PATTERN
  add-proposition --name N --statement S [--aliases A] [--session ID]
  add-chain --premise ID [--premise ID ...] --conclusion ID [--session ID]
  remove ID
  export
"""

from __future__ import annotations

import argparse
import fnmatch
import json
import os
import sys
import time
from pathlib import Path

DEFAULT_DATA_DIR = Path.home() / ".dsh" / "learn"
GRAPH_VERSION = 1


def load_graph(data_dir: Path) -> dict:
    path = data_dir / "graph.json"
    if not path.exists():
        return {"version": GRAPH_VERSION, "propositions": [], "chains": []}
    try:
        graph = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        sys.exit(f"error: cannot read {path}: {exc}")
    version = graph.get("version", 1)
    if version != GRAPH_VERSION:
        sys.exit(f"error: unsupported graph version {version} in {path}")
    graph.setdefault("propositions", [])
    graph.setdefault("chains", [])
    return graph


def save_graph(data_dir: Path, graph: dict) -> None:
    data_dir.mkdir(parents=True, exist_ok=True)
    path = data_dir / "graph.json"
    tmp = path.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.replace(tmp, path)


def next_id(existing: list[str], prefix: str) -> str:
    n = 1
    used = {i for i in existing}
    while f"{prefix}_{n:04d}" in used:
        n += 1
    return f"{prefix}_{n:04d}"


def cmd_stats(args, graph):
    if args.format == "json":
        print(json.dumps({
            "dataDir": str(args.data_dir),
            "propositions": len(graph["propositions"]),
            "chains": len(graph["chains"]),
        }, ensure_ascii=False, indent=2))
        return
    print(f"data dir : {args.data_dir}")
    print(f"propositions : {len(graph['propositions'])}")
    print(f"chains       : {len(graph['chains'])}")


def cmd_propositions(args, graph):
    rows = graph["propositions"]
    if args.session:
        rows = [p for p in rows if any(s == args.session for s in p.get("sessions", []))]
    if args.format == "json":
        print(json.dumps(rows, ensure_ascii=False, indent=2))
        return
    if not rows:
        print("(no propositions)")
        return
    for p in rows:
        aliases = ", ".join(p.get("aliases", []))
        line = f"{p['id']}  {p['name']}" + (f"  [{aliases}]" if aliases else "")
        print(line)
        print(f"    {p['statement']}")
        if p.get("sessions"):
            print(f"    sources: {', '.join(p['sessions'])}")


def cmd_chains(args, graph):
    rows = graph["chains"]
    if args.node:
        rows = [c for c in rows if args.node in c["premises"] or args.node == c["conclusion"]]
    if args.format == "json":
        print(json.dumps(rows, ensure_ascii=False, indent=2))
        return
    if not rows:
        print("(no chains)")
        return
    by_id = {p["id"]: p for p in graph["propositions"]}
    def label(i):
        p = by_id.get(i)
        return f"{i} ({p['name']})" if p else i
    for c in rows:
        print(f"{c['id']}: " + " + ".join(label(x) for x in c["premises"]))
        print(f"    => {label(c['conclusion'])}")
        if c.get("sessions"):
            print(f"    sources: {', '.join(c['sessions'])}")


def cmd_find(args, graph):
    pattern = args.pattern.lower()
    regex = any(ch in pattern for ch in "*?[")
    def match(text):
        text = text.lower()
        return fnmatch.fnmatch(text, f"*{pattern}*") if regex else pattern in text
    props = [p for p in graph["propositions"]
             if match(p["name"]) or match(p["statement"]) or any(match(a) for a in p.get("aliases", []))]
    if args.format == "json":
        print(json.dumps(props, ensure_ascii=False, indent=2))
        return
    if not props:
        print("(no matches)")
        return
    for p in props:
        print(f"{p['id']}  {p['name']}")
        print(f"    {p['statement']}")


def cmd_add_proposition(args, graph):
    ids = [p["id"] for p in graph["propositions"]]
    pid = next_id(ids, "n")
    aliases = [a.strip() for a in args.aliases.split(",")] if args.aliases else []
    sessions = [args.session] if args.session else [time.strftime("%Y-%m-%d")]
    graph["propositions"].append({
        "id": pid, "name": args.name, "statement": args.statement,
        "aliases": aliases, "sessions": sessions, "created": time.strftime("%Y-%m-%dT%H:%M:%S"),
    })
    save_graph(args.data_dir, graph)
    print(pid)


def cmd_add_chain(args, graph):
    by_id = {p["id"] for p in graph["propositions"]}
    missing = [i for i in ([*args.premise, args.conclusion]) if i not in by_id]
    if missing:
        sys.exit(f"error: unknown proposition id(s): {', '.join(missing)}")
    ids = [c["id"] for c in graph["chains"]]
    cid = next_id(ids, "c")
    sessions = [args.session] if args.session else [time.strftime("%Y-%m-%d")]
    graph["chains"].append({
        "id": cid, "premises": args.premise, "conclusion": args.conclusion,
        "sessions": sessions, "created": time.strftime("%Y-%m-%dT%H:%M:%S"),
    })
    save_graph(args.data_dir, graph)
    print(cid)


def cmd_remove(args, graph):
    before_p, before_c = len(graph["propositions"]), len(graph["chains"])
    graph["propositions"] = [p for p in graph["propositions"] if p["id"] != args.id]
    graph["chains"] = [c for c in graph["chains"]
                       if args.id not in c["premises"] and c["conclusion"] != args.id]
    removed = (before_p - len(graph["propositions"])) + (before_c - len(graph["chains"]))
    if not removed:
        sys.exit(f"error: nothing removed; no proposition or chain with id {args.id}")
    save_graph(args.data_dir, graph)
    print(f"removed {removed} record(s)")


def cmd_export(args, graph):
    print(json.dumps(graph, ensure_ascii=False, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--data-dir", default=None, help="graph directory (default ~/.dsh/learn)")
    parser.add_argument("--format", choices=["json", "text"], default="text")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("stats").set_defaults(func=cmd_stats)
    p = sub.add_parser("propositions"); p.add_argument("--session"); p.set_defaults(func=cmd_propositions)
    p = sub.add_parser("chains"); p.add_argument("--node"); p.set_defaults(func=cmd_chains)
    p = sub.add_parser("find"); p.add_argument("pattern"); p.set_defaults(func=cmd_find)
    p = sub.add_parser("add-proposition")
    p.add_argument("--name", required=True); p.add_argument("--statement", required=True)
    p.add_argument("--aliases"); p.add_argument("--session"); p.set_defaults(func=cmd_add_proposition)
    p = sub.add_parser("add-chain")
    p.add_argument("--premise", action="append", required=True)
    p.add_argument("--conclusion", required=True); p.add_argument("--session")
    p.set_defaults(func=cmd_add_chain)
    p = sub.add_parser("remove"); p.add_argument("id"); p.set_defaults(func=cmd_remove)
    sub.add_parser("export").set_defaults(func=cmd_export)
    args = parser.parse_args()
    args.data_dir = Path(args.data_dir).expanduser() if args.data_dir else DEFAULT_DATA_DIR
    args.func(args, load_graph(args.data_dir))


if __name__ == "__main__":
    main()
