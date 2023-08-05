"""Generate build order graph from directory of debian packaging repositories"""

__version__ = "0.7.1"

import argparse
import logging
import re
import sys

from collections import namedtuple
from pathlib import Path
from typing import Dict, List

import networkx as nx

from debian import deb822

L = logging.getLogger("controlgraph")
L.addHandler(logging.NullHandler())


BinaryPackage = namedtuple("BinaryPackage", ["name", "source", "build_deps", "dir"])


def parse_controlfile(path: Path) -> Dict[str, BinaryPackage]:
    """Parse directory containing debian/control"""
    source = ""
    build_deps = []
    pkgs = {}
    file = Path(path / "debian/control")
    with file.open() as control:
        for pg in deb822.Sources.iter_paragraphs(control):
            if "Source" in pg:
                source = pg["Source"]
                if "Build-Depends" in pg:
                    build_deps.extend(
                        [
                            re.sub(r" \([^\)]*\)", "", s.strip()).strip()
                            for s in pg["Build-Depends"].split(",")
                        ]
                    )
            elif "Package" in pg:
                if source != "":
                    pkgs[pg["Package"]] = BinaryPackage(
                        pg["Package"], source, build_deps, path.stem
                    )
                else:
                    pkgs[pg["Package"]] = BinaryPackage(
                        pg["Package"], pg["Package"], build_deps, path.stem
                    )
    return pkgs


def parse_all_controlfiles(dirs: List[Path]) -> Dict[str, BinaryPackage]:
    """Process all repo/debian/control files in a directory"""
    pkgs = {}
    for path in dirs:
        if not Path(path / "debian/control").exists():
            continue
        pkgs.update(parse_controlfile(path))
    return pkgs


def graph(pkgs: Dict[str, BinaryPackage]) -> nx.DiGraph:
    """Builds graph of build dependencies"""
    # To get build dependencies from a source package
    build_deps = {}
    # To get the source package for a binary package
    src_pkgs = {}
    # To get the directory for a source package
    directories = {}

    # Build maps mentioned above
    for _, pkg in pkgs.items():
        build_deps[pkg.source] = pkg.build_deps
        src_pkgs[pkg.name] = pkg.source
        directories[pkg.source] = pkg.dir

    # Convert binary build dependencies to local directories
    for src, d in directories.items():
        src_deps = []
        for dep in build_deps[src]:
            if dep in src_pkgs:
                src_deps.append(directories[src_pkgs[dep]])
        build_deps[src] = src_deps

    # Create graph from build dependencies
    dep_graph = nx.DiGraph()
    for src, d in directories.items():
        dep_graph.add_node(d)
        dep_graph.add_nodes_from(build_deps[src])
        for dep in build_deps[src]:
            dep_graph.add_edge(d, dep)

    return dep_graph


def main() -> int:
    """Parse args, generate graph, and print it"""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--version", "-V", action="store_true", help="print program version"
    )
    parser.add_argument(
        "--verbose", "-v", help="-v for info, -vv for debug", action="count", default=0
    )
    parser.add_argument(
        "--danglers-first",
        action="store_true",
        help="list all independent repositories first",
    )
    parser.add_argument(
        "--danglers-only",
        action="store_true",
        help="only list independent repositories",
    )
    parser.add_argument(
        "--no-danglers",
        action="store_true",
        help="drop all independent repositories from graph",
    )
    parser.add_argument(
        "--graph",
        "-g",
        action="store_true",
        help="return dot graph of build dependencies",
    )
    parser.add_argument(
        "--reverse",
        "-r",
        action="store_true",
        help="reverse output, only works with --graph, shows parallel build stream",
    )
    parser.add_argument(
        "directories", type=Path, nargs="*", help="directories to graph"
    )
    args = parser.parse_args()

    if args.version:
        print("controlgraph {}".format(__version__))
        return 0

    # set up logging
    logging.basicConfig(
        format="[%(levelname)s] %(message)s", level=10 * (3 - min(args.verbose, 2))
    )

    if not args.directories:
        args.directories = [p for p in Path.cwd().iterdir() if p.is_dir()]

    # Get graph and print
    dep_graph = graph(parse_all_controlfiles(args.directories))
    if args.no_danglers:
        isolates = list(nx.isolates(dep_graph))
        dep_graph.remove_nodes_from(isolates)

    if args.graph:
        if args.reverse:
            dep_graph = dep_graph.reverse()
        nx.nx_pydot.write_dot(dep_graph, sys.stdout)
    else:
        if args.danglers_first:
            # Put all isolated nodes first in list
            isolates = list(nx.isolates(dep_graph))
            dep_graph.remove_nodes_from(isolates)
            build_order = list(nx.dfs_postorder_nodes(dep_graph))
            print(" ".join(isolates + build_order))
        elif args.danglers_only:
            print(" ".join(list(nx.isolates(dep_graph))))
        else:
            print(" ".join(list(nx.dfs_postorder_nodes(dep_graph))))

    return 0


if __name__ == "__main__":
    sys.exit(main())
