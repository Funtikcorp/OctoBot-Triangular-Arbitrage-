from dataclasses import dataclass

@dataclass
class Symbol:
    value: str

    def __post_init__(self):
        if '/' not in self.value:
            raise ValueError('Symbol must be formatted as BASE/QUOTE')
        self.base, self.quote = self.value.split('/')

    def __str__(self):
        return self.value

def parse_symbol(symbol_str: str) -> Symbol:
    return Symbol(symbol_str)
