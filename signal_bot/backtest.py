import pandas as pd

from signal_bot.engine import generate_signal


def _calculate_drawdown(equity_curve: list[float]) -> float:
    peak = equity_curve[0] if equity_curve else 0.0
    max_drawdown = 0.0
    for equity in equity_curve:
        peak = max(peak, equity)
        if peak > 0:
            drawdown = ((peak - equity) / peak) * 100
            max_drawdown = max(max_drawdown, drawdown)
    return round(max_drawdown, 2)


def run_backtest(df: pd.DataFrame, config: dict) -> dict:
    trades = []
    risk_cfg = config.get("risk", {})
    backtest_cfg = config.get("backtest", {})

    equity = float(risk_cfg.get("paper_balance", 1000))
    risk_per_trade_pct = float(risk_cfg.get("risk_per_trade_pct", 1.0))
    spread_points = float(backtest_cfg.get("spread_points", 0.2))
    slippage_points = float(backtest_cfg.get("slippage_points", 0.1))
    max_hold_bars = int(backtest_cfg.get("max_hold_bars", 3))
    point_value = float(backtest_cfg.get("point_value", 1.0))

    equity_curve = [equity]

    for end_idx in range(60, len(df) - 1):
        window = df.iloc[: end_idx + 1].copy()
        signal_data = generate_signal(window, config)
        signal = signal_data["signal"]
        if signal not in ("BUY", "SELL"):
            continue

        raw_entry = float(signal_data["entry_hint"])
        sl = signal_data["stop_loss"]
        tp = signal_data["take_profit"]
        if sl is None or tp is None:
            continue

        entry = raw_entry + spread_points / 2 if signal == "BUY" else raw_entry - spread_points / 2
        risk_amount = equity * (risk_per_trade_pct / 100)
        stop_distance = abs(entry - float(sl))
        if stop_distance <= 0:
            continue

        position_size = risk_amount / stop_distance
        result = "FLAT"
        exit_price = entry
        exit_index = end_idx + 1

        for future_idx in range(end_idx + 1, min(len(df), end_idx + 1 + max_hold_bars)):
            bar = df.iloc[future_idx]
            exit_index = future_idx

            if signal == "BUY":
                if float(bar["low"]) <= float(sl):
                    result = "LOSS"
                    exit_price = float(sl) - slippage_points
                    break
                if float(bar["high"]) >= float(tp):
                    result = "WIN"
                    exit_price = float(tp) - slippage_points
                    break
                exit_price = float(bar["close"]) - spread_points / 2
            else:
                if float(bar["high"]) >= float(sl):
                    result = "LOSS"
                    exit_price = float(sl) + slippage_points
                    break
                if float(bar["low"]) <= float(tp):
                    result = "WIN"
                    exit_price = float(tp) + slippage_points
                    break
                exit_price = float(bar["close"]) + spread_points / 2

        pnl_points = (exit_price - entry) if signal == "BUY" else (entry - exit_price)
        pnl = pnl_points * position_size * point_value
        equity += pnl
        equity_curve.append(equity)

        trades.append(
            {
                "index": end_idx,
                "exit_index": exit_index,
                "signal": signal,
                "entry": round(entry, 4),
                "sl": round(float(sl), 4),
                "tp": round(float(tp), 4),
                "exit": round(exit_price, 4),
                "position_size": round(position_size, 4),
                "result": result,
                "pnl": round(pnl, 4),
                "equity": round(equity, 4),
            }
        )

    total = len(trades)
    wins = sum(1 for t in trades if t["result"] == "WIN")
    losses = sum(1 for t in trades if t["result"] == "LOSS")
    flats = sum(1 for t in trades if t["result"] == "FLAT")
    gross_profit = sum(t["pnl"] for t in trades if t["pnl"] > 0)
    gross_loss = abs(sum(t["pnl"] for t in trades if t["pnl"] < 0))
    profit_factor = round(gross_profit / gross_loss, 2) if gross_loss > 0 else None
    win_rate = (wins / total * 100) if total else 0.0
    net_pnl = sum(t["pnl"] for t in trades)
    max_drawdown_pct = _calculate_drawdown(equity_curve)

    return {
        "total_trades": total,
        "wins": wins,
        "losses": losses,
        "flats": flats,
        "win_rate_pct": round(win_rate, 2),
        "net_pnl": round(net_pnl, 4),
        "ending_equity": round(equity, 4),
        "profit_factor": profit_factor,
        "max_drawdown_pct": max_drawdown_pct,
        "equity_curve": [round(x, 4) for x in equity_curve],
        "trades": trades,
    }
