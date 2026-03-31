import pandas as pd

from signal_bot.engine import generate_signal


def run_backtest(df: pd.DataFrame, config: dict) -> dict:
    trades = []
    equity = float(config.get("risk", {}).get("paper_balance", 1000))

    for end_idx in range(60, len(df) - 1):
        window = df.iloc[: end_idx + 1].copy()
        signal_data = generate_signal(window, config)
        signal = signal_data["signal"]
        if signal not in ("BUY", "SELL"):
            continue

        entry = float(signal_data["entry_hint"])
        sl = signal_data["stop_loss"]
        tp = signal_data["take_profit"]
        if sl is None or tp is None:
            continue

        next_bar = df.iloc[end_idx + 1]
        result = "OPEN"
        exit_price = float(next_bar["close"])

        if signal == "BUY":
            if float(next_bar["low"]) <= float(sl):
                result = "LOSS"
                exit_price = float(sl)
            elif float(next_bar["high"]) >= float(tp):
                result = "WIN"
                exit_price = float(tp)
            else:
                result = "FLAT"
        elif signal == "SELL":
            if float(next_bar["high"]) >= float(sl):
                result = "LOSS"
                exit_price = float(sl)
            elif float(next_bar["low"]) <= float(tp):
                result = "WIN"
                exit_price = float(tp)
            else:
                result = "FLAT"

        pnl = 0.0
        if signal == "BUY":
            pnl = exit_price - entry
        elif signal == "SELL":
            pnl = entry - exit_price

        equity += pnl
        trades.append(
            {
                "index": end_idx,
                "signal": signal,
                "entry": entry,
                "sl": sl,
                "tp": tp,
                "exit": exit_price,
                "result": result,
                "pnl": pnl,
                "equity": equity,
            }
        )

    total = len(trades)
    wins = sum(1 for t in trades if t["result"] == "WIN")
    losses = sum(1 for t in trades if t["result"] == "LOSS")
    flats = sum(1 for t in trades if t["result"] == "FLAT")
    win_rate = (wins / total * 100) if total else 0.0
    net_pnl = sum(t["pnl"] for t in trades)

    return {
        "total_trades": total,
        "wins": wins,
        "losses": losses,
        "flats": flats,
        "win_rate_pct": round(win_rate, 2),
        "net_pnl": round(net_pnl, 4),
        "ending_equity": round(equity, 4),
        "trades": trades,
    }
