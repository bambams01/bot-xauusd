from signal_bot.config import load_config
from signal_bot.engine import generate_signal
from signal_bot.sample_data import load_sample_ohlcv


def main():
    config = load_config("config.yaml")
    candles = load_sample_ohlcv()
    result = generate_signal(candles, config)
    print(result)


if __name__ == "__main__":
    main()
