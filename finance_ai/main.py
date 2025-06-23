"""Entry point for running the multi-agent trading system."""

from .graph import TradingGraph


def main() -> None:
    """Instantiate and run the trading graph."""
    graph = TradingGraph()
    result = graph.run()
    print(result)


if __name__ == "__main__":
    main()
