class BaseExchange:
    has = {"fetchTickers": True}

    async def fetch_tickers(self):
        return {}

    def milliseconds(self):
        import time
        return int(time.time() * 1000)

    async def close(self):
        pass
