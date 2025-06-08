import argparse
import asyncio

from triangular_arbitrage import detector


def create_parser() -> argparse.ArgumentParser:
    """Return the argument parser for the CLI."""
    parser = argparse.ArgumentParser(description="OctoBot triangular arbitrage detector")
    parser.add_argument("--exchange", default="binanceus",
                        help="Exchange id from ccxt list (e.g. binanceus)")
    parser.add_argument("--max-cycle", type=int, default=10,
                        help="Maximum number of symbols in a detection cycle")
    parser.add_argument("--ignored-symbols", nargs="*", default=[],
                        help="Symbols to ignore during detection")
    parser.add_argument("--whitelisted-symbols", nargs="*", default=None,
                        help="Optional list of allowed symbols")
    parser.add_argument("--benchmark", action="store_true",
                        help="Display execution time")
    return parser


def parse_arguments(args=None):
    """Parse command line arguments."""
    return create_parser().parse_args(args)


def run_from_command_line(args=None):
    """Run the detector using command line arguments."""
    parsed = parse_arguments(args)

    if hasattr(asyncio, "WindowsSelectorEventLoopPolicy"):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    if parsed.benchmark:
        import time
        start = time.perf_counter()

    print("Scanning...")
    best_opportunities, best_profit = asyncio.run(
        detector.run_detection(
            parsed.exchange,
            ignored_symbols=parsed.ignored_symbols,
            whitelisted_symbols=parsed.whitelisted_symbols,
            max_cycle=parsed.max_cycle,
        )
    )

    def get_order_side(opportunity: detector.ShortTicker):
        return "buy" if opportunity.reversed else "sell"

    if best_opportunities is not None:
        print("-------------------------------------------")
        total_profit_percentage = round((best_profit - 1) * 100, 5)
        print(f"New {total_profit_percentage}% {parsed.exchange} opportunity:")
        for i, opportunity in enumerate(best_opportunities):
            order_side = get_order_side(opportunity)
            base_currency = opportunity.symbol.base
            quote_currency = opportunity.symbol.quote
            print(
                f"{i + 1}. {order_side} {base_currency} "
                f"{'with' if order_side == 'buy' else 'for'} "
                f"{quote_currency} at {opportunity.last_price:.5f}"
            )
        print("-------------------------------------------")
    else:
        print("No opportunity detected")

    if parsed.benchmark:
        elapsed = time.perf_counter() - start
        print(f"{__file__} executed in {elapsed:0.2f} seconds.")


if __name__ == "__main__":
    run_from_command_line()
