class Symbol:
    def __init__(self, pair: str):
        self.pair = pair
        parts = pair.split('/')
        self.base = parts[0]
        self.quote = parts[1] if len(parts) > 1 else ''

    def __str__(self):
        return self.pair

def parse_symbol(pair: str) -> 'Symbol':
    return Symbol(pair)
