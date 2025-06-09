from dataclasses import dataclass

@dataclass
class Symbol:
    base: str
    quote: str

    def __init__(self, symbol: str):
        if '/' not in symbol:
            raise ValueError("Invalid symbol format")
        self.base, self.quote = symbol.split('/', 1)

    def __str__(self):
        return f"{self.base}/{self.quote}"

def parse_symbol(value: str) -> Symbol:
    """Parse a symbol string like 'BTC/USDT'.

    Raises ValueError if the format is invalid.
    """
    if not isinstance(value, str) or '/' not in value:
        raise ValueError("Invalid symbol format")
    return Symbol(value)
