class DiGraph:
    def __init__(self):
        self.adj = {}

    def add_edge(self, u, v, **attrs):
        self.adj.setdefault(u, {})[v] = attrs

    def __getitem__(self, item):
        return self.adj[item]

    def nodes(self):
        return list(self.adj.keys())

def _canonical(cycle):
    if not cycle:
        return ()
    min_index = min(range(len(cycle)), key=lambda i: str(cycle[i]))
    rotated = cycle[min_index:] + cycle[:min_index]
    return tuple(rotated)

def simple_cycles(graph):
    cycles = []

    def dfs(start, current, path, visited):
        visited.add(current)
        path.append(current)
        for neighbor in graph.adj.get(current, {}):
            if neighbor == start:
                cycles.append(list(path))
            elif neighbor not in visited:
                dfs(start, neighbor, path, visited)
        path.pop()
        visited.discard(current)

    for node in list(graph.nodes()):
        dfs(node, node, [], set())

    uniques = []
    seen = set()
    for cyc in cycles:
        canon = _canonical(cyc)
        if canon not in seen:
            seen.add(canon)
            uniques.append(cyc)
    return uniques
