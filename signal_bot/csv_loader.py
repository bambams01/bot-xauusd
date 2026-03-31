import pandas as pd


def load_ohlcv_csv(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    columns = {c.lower(): c for c in df.columns}
    required = ["open", "high", "low", "close"]
    for key in required:
        if key not in columns:
            raise ValueError(f"Missing required column: {key}")

    normalized = pd.DataFrame(
        {
            "open": df[columns["open"]],
            "high": df[columns["high"]],
            "low": df[columns["low"]],
            "close": df[columns["close"]],
            "volume": df[columns["volume"]] if "volume" in columns else 0,
        }
    )
    return normalized
