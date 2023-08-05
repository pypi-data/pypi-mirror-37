# controlgraph

[![PyPI version](https://badge.fury.io/py/controlgraph.svg)](https://pypi.org/project/controlgraph/)
[![Build status](https://badge.buildkite.com/81c4e486b5f9ff5d3bf3f3da820201cefad4965207f4e2a8c2.svg)](https://buildkite.com/opx/opx-infra-controlgraph)

controlgraph is a directed graph which can be traversed to enable parallelized Debian package builds.

From the available directories with valid Debian packaging, a graph with directories (representing source packages) for nodes and build dependencies for edges is produced. The reverse of this graph can traversed with a breadth-first search to build in dependency order.

`controlgraph` is a program which returns the controlgraph for a directory to build, in linear or dot format.

## Installation

```bash
pip3 install controlgraph
```

## Library Usage

```python3
import sys

from pathlib import Path

import controlgraph
import networkx as nx

# get all directories
dirs = [p for p in Path.cwd().iterdir() if p.is_dir()]

# get map of local binary packages to locally-available source build dependencies
pkgs = controlgraph.parse_all_controlfiles(dirs)

# generate build dependency graph from map
dep_graph = controlgraph.graph(pkgs)

# print full dot graph
nx.nx_pydot.write_dot(dep_graph, sys.stdout)

# print linear order from depth-first search
print(" ".join(list(nx.dfs_postorder_nodes(dep_graph))))
```

Output

```
strict digraph  {
"opx-nas-daemon";
"opx-common-utils";
"opx-cps";
"opx-logging";
"opx-nas-acl";
"opx-sdi-sys";
"opx-nas-daemon" -> "opx-common-utils";
"opx-nas-daemon" -> "opx-cps";
"opx-nas-daemon" -> "opx-logging";
"opx-nas-daemon" -> "opx-nas-acl";
"opx-common-utils" -> "opx-logging";
"opx-cps" -> "opx-common-utils";
"opx-cps" -> "opx-logging";
"opx-nas-acl" -> "opx-common-utils";
"opx-nas-acl" -> "opx-cps";
"opx-nas-acl" -> "opx-logging";
"opx-sdi-sys" -> "opx-common-utils";
"opx-sdi-sys" -> "opx-logging";
}

opx-logging opx-common-utils opx-cps opx-nas-acl opx-nas-daemon opx-sdi-sys
```

## CLI Usage

With one or more directories present, run `controlgraph`.

```bash
$ for r in opx-nas-acl opx-nas-daemon opx-alarm opx-logging opx-common-utils; do
    git clone "https://github.com/open-switch/$r"
  done

$ controlgraph
opx-alarm opx-logging opx-common-utils opx-nas-acl opx-nas-daemon

$ controlgraph --graph
strict digraph  {
"opx-alarm";
"opx-nas-daemon";
"opx-common-utils";
"opx-logging";
"opx-nas-acl";
"opx-nas-daemon" -> "opx-common-utils";
"opx-nas-daemon" -> "opx-logging";
"opx-nas-daemon" -> "opx-nas-acl";
"opx-common-utils" -> "opx-logging";
"opx-nas-acl" -> "opx-common-utils";
"opx-nas-acl" -> "opx-logging";
}
```
