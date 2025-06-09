class DiGraph:
    def __init__(self):
        self.adj = {}

    def add_edge(self, u, v, **attrs):
        self.adj.setdefault(u, {})[v] = attrs

    def __getitem__(self, item):
        return self.adj[item]


def simple_cycles(graph):
    adjacency = graph.adj
    all_cycles = []
    path = []

    def dfs(start, current, visited):
        visited.append(current)
        for neighbor in adjacency.get(current, {}):
            if neighbor == start:
                all_cycles.append(visited.copy())
            elif neighbor not in visited:
                dfs(start, neighbor, visited.copy())
        visited.pop()

    for node in adjacency:
        dfs(node, node, [])

    unique = []
    seen = set()
    for cycle in all_cycles:
        # normalize cycle by rotation to smallest representation
        min_idx = min(range(len(cycle)), key=lambda i: cycle[i])
        normalized = tuple(cycle[min_idx:] + cycle[:min_idx])
        if normalized not in seen:
            seen.add(normalized)
            unique.append(cycle)
    return unique
