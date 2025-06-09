class DiGraph:
    def __init__(self):
        self.edges = {}

    def add_edge(self, u, v, ticker=None):
        self.edges.setdefault(u, {})[v] = {'ticker': ticker}

    def __getitem__(self, item):
        return self.edges[item]


def simple_cycles(graph):
    visited = set()
    cycles = []
    for start in list(graph.edges):
        stack = [(start, [start])]
        while stack:
            node, path = stack.pop()
            for succ in graph.edges.get(node, {}):
                if succ == path[0] and len(path) > 1:
                    cycles.append(path)
                elif succ not in path:
                    stack.append((succ, path + [succ]))
    # remove duplicate cycles ignoring rotation
    unique = []
    seen = set()
    for c in cycles:
        normalized = tuple(sorted(c))
        if normalized not in seen:
            seen.add(normalized)
            unique.append(c)
    return unique
