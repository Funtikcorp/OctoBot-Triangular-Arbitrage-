import sys
import types
from dataclasses import dataclass

# Provide minimal stubs for external dependencies so tests can run without them

# octobot_commons.symbols
symbols_mod = types.ModuleType("octobot_commons.symbols")
@dataclass
class Symbol:
    base: str = ""
    quote: str = ""

    def __init__(self, symbol: str):
        self.base, self.quote = symbol.split("/")

    def __str__(self):
        return f"{self.base}/{self.quote}"

def parse_symbol(value: str) -> Symbol:
    return Symbol(value)

symbols_mod.Symbol = Symbol
symbols_mod.parse_symbol = parse_symbol
sys.modules["octobot_commons.symbols"] = symbols_mod

commons_pkg = types.ModuleType("octobot_commons")
commons_pkg.symbols = symbols_mod

# octobot_commons.constants
constants_mod = types.ModuleType("octobot_commons.constants")
constants_mod.DAYS_TO_SECONDS = 86400
constants_mod.MSECONDS_TO_SECONDS = 0.001
constants_mod.MILLISECONDS_TO_SECONDS = 0.001
sys.modules["octobot_commons.constants"] = constants_mod
commons_pkg.constants = constants_mod
sys.modules["octobot_commons"] = commons_pkg

# minimal networkx
nx_mod = types.ModuleType("networkx")
class DiGraph:
    def __init__(self):
        self.adj = {}
    def add_edge(self, u, v, **kwargs):
        self.adj.setdefault(u, {})[v] = kwargs
    def __getitem__(self, item):
        return self.adj[item]

nx_mod.DiGraph = DiGraph

def simple_cycles(graph):
    cycles = []
    path = []
    def dfs(node, start):
        path.append(node)
        for neighbour in graph.adj.get(node, {}):
            if neighbour == start:
                cycles.append(path.copy())
            elif neighbour not in path:
                dfs(neighbour, start)
        path.pop()
    for n in list(graph.adj):
        dfs(n, n)
    return cycles

nx_mod.simple_cycles = simple_cycles
sys.modules['networkx'] = nx_mod

# ccxt.async_support stub
ccxt_mod = types.ModuleType('ccxt.async_support')
class BaseError(Exception):
    pass
ccxt_mod.BaseError = BaseError
sys.modules['ccxt.async_support'] = ccxt_mod
ccxt_pkg = types.ModuleType('ccxt')
ccxt_pkg.async_support = ccxt_mod
ccxt_pkg.BaseError = BaseError
sys.modules['ccxt'] = ccxt_pkg
