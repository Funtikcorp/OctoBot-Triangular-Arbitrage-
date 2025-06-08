from dataclasses import dataclass

@dataclass
class Symbol:
    raw: str
    base: str
    quote: str

    def __init__(self, symbol: str):
        if '/' not in symbol:
            raise ValueError(f"Invalid symbol format: {symbol}")
        self.raw = symbol
        self.base, self.quote = symbol.split('/')

    def __str__(self):
        return self.raw

def parse_symbol(symbol: str) -> Symbol:
    return Symbol(symbol)
