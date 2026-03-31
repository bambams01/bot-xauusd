import argparse

from signal_bot.backtest import run_backtest
from signal_bot.config import load_config
from signal_bot.csv_loader import load_ohlcv_csv
from signal_bot.sample_data import load_sample_ohlcv


def main():
    parser = argparse.ArgumentParser(description="Run XAUUSD backtest")
    parser.add_argument("--csv", default=None, help="Path to OHLCV CSV")
    parser.add_argument("--config", default="config.yaml", help="Path to config file")
    args = parser.parse_args()

    config = load_config(args.config)
    candles = load_ohlcv_csv(args.csv) if args.csv else load_sample_ohlcv()
    result = run_backtest(candles, config)
    summary = {
        "total_trades": result["total_trades"],
        "wins": result["wins"],
        "losses": result["losses"],
        "flats": result["flats"],
        "win_rate_pct": result["win_rate_pct"],
        "net_pnl": result["net_pnl"],
        "ending_equity": result["ending_equity"],
        "profit_factor": result["profit_factor"],
        "max_drawdown_pct": result["max_drawdown_pct"],
    }
    print(summary)


if __name__ == "__main__":
    main()
