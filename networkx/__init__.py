class DiGraph:
    def __init__(self):
        self._adj = {}

    def add_edge(self, u, v, **attr):
        self._adj.setdefault(u, {})[v] = attr

    def __getitem__(self, node):
        return self._adj[node]

    def nodes(self):
        nodes = set(self._adj.keys())
        for edges in self._adj.values():
            nodes.update(edges.keys())
        return list(nodes)

    def neighbors(self, node):
        return self._adj.get(node, {})


def simple_cycles(graph):
    cycles = []
    def dfs(start, node, path):
        path.append(node)
        for neigh in graph.neighbors(node):
            if neigh == start:
                cycles.append(path.copy())
            elif neigh not in path:
                dfs(start, neigh, path)
        path.pop()

    for node in graph.nodes():
        dfs(node, node, [])

    unique = []
    seen = set()
    for cycle in cycles:
        if not cycle:
            continue
        # canonical representation: rotate to minimal string
        min_index = min(range(len(cycle)), key=lambda i: str(cycle[i]))
        canon = tuple(cycle[min_index:] + cycle[:min_index])
        if canon not in seen:
            seen.add(canon)
            unique.append(list(canon))
    return unique
