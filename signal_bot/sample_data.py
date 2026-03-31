import pandas as pd


def load_sample_ohlcv() -> pd.DataFrame:
    rows = []
    base = 2300.0
    for i in range(120):
        open_ = base + (i * 0.15)
        high = open_ + 1.2
        low = open_ - 0.8
        close = open_ + (0.3 if i % 3 else -0.2)
        rows.append({
            'open': open_,
            'high': high,
            'low': low,
            'close': close,
            'volume': 100 + i,
        })
    return pd.DataFrame(rows)
