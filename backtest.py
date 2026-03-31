from signal_bot.config import load_config
from signal_bot.sample_data import load_sample_ohlcv
from signal_bot.backtest import run_backtest


def main():
    config = load_config("config.yaml")
    candles = load_sample_ohlcv()
    result = run_backtest(candles, config)
    summary = {
        "total_trades": result["total_trades"],
        "wins": result["wins"],
        "losses": result["losses"],
        "flats": result["flats"],
        "win_rate_pct": result["win_rate_pct"],
        "net_pnl": result["net_pnl"],
        "ending_equity": result["ending_equity"],
    }
    print(summary)


if __name__ == "__main__":
    main()
