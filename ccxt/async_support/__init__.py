class Exchange:
    def __init__(self):
        self.has = {'fetchTickers': False}

    async def fetch_tickers(self):
        return []

    def milliseconds(self):
        return 0

    async def close(self):
        pass
