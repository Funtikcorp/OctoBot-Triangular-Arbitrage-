import asyncio
import pytest
import octobot_commons.symbols as symbols
from triangular_arbitrage.detector import (
    ShortTicker,
    get_best_triangular_opportunity,
    get_best_opportunity,
    get_exchange_data,
    TickerFetchError,
)


@pytest.fixture
def sample_tickers():
    return [
        ShortTicker(symbol=symbols.Symbol('BTC/USDT'), last_price=30000),
        ShortTicker(symbol=symbols.Symbol('ETH/USDT'), last_price=2000),
        ShortTicker(symbol=symbols.Symbol('XRP/USDT'), last_price=0.5),
        ShortTicker(symbol=symbols.Symbol('LTC/USDT'), last_price=100),
        ShortTicker(symbol=symbols.Symbol('BCH/USDT'), last_price=200),
    ]


def test_get_best_triangular_opportunity_handles_empty_tickers():
    best_opportunity, best_profit = get_best_triangular_opportunity([])
    assert best_profit == 1
    assert best_opportunity is None


def test_get_best_triangular_opportunity_handles_no_cycle_opportunity(sample_tickers):
    sample_tickers.append(ShortTicker(symbol=symbols.Symbol('DOT/USDT'), last_price=0.05))
    best_opportunity, best_profit = get_best_triangular_opportunity(sample_tickers)
    assert best_profit == 1
    assert best_opportunity is None

def test_get_best_opportunity_handles_empty_tickers():
    best_opportunity, best_profit = get_best_opportunity([])
    assert best_profit == 1
    assert best_opportunity is None


def test_get_best_opportunity_handles_no_triplet_opportunity(sample_tickers):
    sample_tickers.append(ShortTicker(symbol=symbols.Symbol('DOT/USDT'), last_price=0.05))
    best_opportunity, best_profit = get_best_opportunity(sample_tickers)
    assert best_profit == 1
    assert best_opportunity is None


def test_get_best_opportunity_returns_correct_triplet_with_correct_tickers():
    tickers = [
        ShortTicker(symbol=symbols.Symbol('BTC/USDT'), last_price=30000),
        ShortTicker(symbol=symbols.Symbol('ETH/BTC'), last_price=0.3),
        ShortTicker(symbol=symbols.Symbol('ETH/USDT'), last_price=2000),
    ]
    best_opportunity, best_profit = get_best_triangular_opportunity(tickers)
    assert len(best_opportunity) == 3
    assert best_profit == 4.5
    assert all(isinstance(ticker, ShortTicker) for ticker in best_opportunity)


def test_get_best_opportunity_returns_correct_triplet_with_multiple_tickers():
    tickers = [
        ShortTicker(symbol=symbols.Symbol('BTC/USDT'), last_price=30000),
        ShortTicker(symbol=symbols.Symbol('ETH/BTC'), last_price=0.3),
        ShortTicker(symbol=symbols.Symbol('ETH/USDT'), last_price=2000),
        ShortTicker(symbol=symbols.Symbol('ETH/USDC'), last_price=1900),
        ShortTicker(symbol=symbols.Symbol('BTC/USDC'), last_price=35000),
        ShortTicker(symbol=symbols.Symbol('USDC/USDT'), last_price=1.1),
        ShortTicker(symbol=symbols.Symbol('USDC/TUSD'), last_price=0.95),
        ShortTicker(symbol=symbols.Symbol('ETH/TUSD'), last_price=1950),
        ShortTicker(symbol=symbols.Symbol('BTC/TUSD'), last_price=32500),
    ]
    best_opportunity, best_profit = get_best_triangular_opportunity(tickers)
    assert len(best_opportunity) == 3
    assert round(best_profit, 3) == 5.526 # 5.526315789473684
    assert all(isinstance(ticker, ShortTicker) for ticker in best_opportunity)

def test_get_best_opportunity_returns_correct_cycle_with_correct_tickers():
    tickers = [
        ShortTicker(symbol=symbols.Symbol('BTC/USDT'), last_price=30000),
        ShortTicker(symbol=symbols.Symbol('ETH/BTC'), last_price=0.3),
        ShortTicker(symbol=symbols.Symbol('ETH/USDT'), last_price=2000),
    ]
    best_opportunity, best_profit = get_best_opportunity(tickers)
    assert len(best_opportunity) >= 3  # Handling cycles with more than 3 tickers
    assert best_profit == 4.5
    assert all(isinstance(ticker, ShortTicker) for ticker in best_opportunity)


def test_get_best_opportunity_returns_correct_cycle_with_multiple_tickers():
    tickers = [
        ShortTicker(symbol=symbols.Symbol('BTC/USDT'), last_price=30000),
        ShortTicker(symbol=symbols.Symbol('ETH/BTC'), last_price=0.3),
        ShortTicker(symbol=symbols.Symbol('ETH/USDT'), last_price=2000),
        ShortTicker(symbol=symbols.Symbol('ETH/USDC'), last_price=1900),
        ShortTicker(symbol=symbols.Symbol('BTC/USDC'), last_price=35000),
        ShortTicker(symbol=symbols.Symbol('USDC/USDT'), last_price=1.1),
        ShortTicker(symbol=symbols.Symbol('USDC/TUSD'), last_price=0.95),
        ShortTicker(symbol=symbols.Symbol('ETH/TUSD'), last_price=1950),
        ShortTicker(symbol=symbols.Symbol('BTC/TUSD'), last_price=32500),
    ]
    best_opportunity, best_profit = get_best_opportunity(tickers)
    assert len(best_opportunity) >= 3  # Handling cycles with more than 3 tickers
    assert round(best_profit, 3) == 5.775
    assert all(isinstance(ticker, ShortTicker) for ticker in best_opportunity)


def test_get_exchange_data_reports_fetch_error(monkeypatch):
    class FailingExchange:
        has = {'fetchTickers': True}

        async def fetch_tickers(self):
            raise get_exchange_data.__globals__['ccxt'].BaseError('fail')

        def milliseconds(self):
            return 0

        async def close(self):
            pass

    monkeypatch.setattr(
        get_exchange_data.__globals__['ccxt'],
        'binanceus',
        FailingExchange,
        raising=False,
    )

    with pytest.raises(TickerFetchError):
        asyncio.run(get_exchange_data('binanceus'))


def test_get_exchange_data_reports_instantiation_error(monkeypatch):
    class BadExchange:
        def __init__(self):
            raise get_exchange_data.__globals__['ccxt'].BaseError('boom')

    monkeypatch.setattr(
        get_exchange_data.__globals__['ccxt'],
        'badexchange',
        BadExchange,
        raising=False,
    )

    with pytest.raises(TickerFetchError):
        asyncio.run(get_exchange_data('badexchange'))
