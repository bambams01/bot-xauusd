import pandas as pd

from signal_bot.indicators import ema, rsi, atr


def generate_signal(df: pd.DataFrame, config: dict) -> dict:
    strategy = config["strategy"]

    data = df.copy()
    data["ema_fast"] = ema(data["close"], strategy["ema_fast"])
    data["ema_slow"] = ema(data["close"], strategy["ema_slow"])
    data["rsi"] = rsi(data["close"], strategy["rsi_period"])
    data["atr"] = atr(data, strategy["atr_period"])

    row = data.iloc[-1]
    price = float(row["close"])
    ema_fast_v = float(row["ema_fast"])
    ema_slow_v = float(row["ema_slow"])
    rsi_v = float(row["rsi"])
    atr_v = float(row["atr"])

    signal = "HOLD"
    reason = []

    if atr_v >= strategy["min_atr"]:
        if ema_fast_v > ema_slow_v and price >= ema_fast_v and rsi_v >= strategy["rsi_buy_threshold"]:
            signal = "BUY"
            reason.append("trend_up")
            reason.append("rsi_confirmed")
        elif ema_fast_v < ema_slow_v and price <= ema_fast_v and rsi_v <= strategy["rsi_sell_threshold"]:
            signal = "SELL"
            reason.append("trend_down")
            reason.append("rsi_confirmed")
        else:
            reason.append("conditions_not_met")
    else:
        reason.append("atr_too_low")

    sl = None
    tp = None
    if signal == "BUY":
        sl = price - (atr_v * strategy["atr_sl_multiplier"])
        tp = price + (atr_v * strategy["atr_tp_multiplier"])
    elif signal == "SELL":
        sl = price + (atr_v * strategy["atr_sl_multiplier"])
        tp = price - (atr_v * strategy["atr_tp_multiplier"])

    return {
        "symbol": config.get("symbol", "XAUUSD"),
        "timeframe": config.get("timeframe", "5m"),
        "signal": signal,
        "entry_hint": round(price, 4),
        "stop_loss": round(sl, 4) if sl is not None else None,
        "take_profit": round(tp, 4) if tp is not None else None,
        "indicators": {
            "ema_fast": round(ema_fast_v, 4),
            "ema_slow": round(ema_slow_v, 4),
            "rsi": round(rsi_v, 4),
            "atr": round(atr_v, 4),
        },
        "reason": reason,
    }
