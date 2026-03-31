# bot-xauusd

Signal bot XAUUSD untuk riset, paper testing, dan pengembangan strategi.

## Fokus proyek
- Bukan auto-execution live trading
- Fokus pada signal generation
- Backtest-ready
- Paper-trade friendly
- Cocok untuk TF 5m

## Strategi awal
Strategi baseline menggunakan kombinasi:
- EMA trend filter
- RSI pullback confirmation
- ATR untuk stop loss / take profit berbasis volatilitas
- Session filter opsional

## Aturan dasar signal
### Buy setup
- EMA fast > EMA slow
- harga pullback ke area EMA fast
- RSI rebound dari area lemah ke atas threshold
- volatilitas memadai

### Sell setup
- EMA fast < EMA slow
- harga pullback ke area EMA fast
- RSI turun dari area kuat ke bawah threshold
- volatilitas memadai

## Output
- signal: BUY / SELL / HOLD
- entry hint
- stop loss hint
- take profit hint
- reason / debug data

## Backtest
Tersedia backtest yang lebih realistis dengan komponen dasar:
- spread
- slippage
- max hold bars
- position sizing sederhana berbasis risk percent
- profit factor
- max drawdown

Jalankan dengan sample data:
```bash
python backtest.py
```

Jalankan dengan CSV sendiri:
```bash
python backtest.py --csv sample_xauusd.csv
```

Jika ingin memakai data CSV sendiri, loader sudah disiapkan di `signal_bot/csv_loader.py`.
Format contoh ada di `examples/mt5_export_format.csv`.

## Disclaimer
Bot ini untuk riset dan paper testing. Tidak menjamin profit atau win rate tertentu.

## Catatan runtime
Jika ada error dependency numerik di environment tertentu, gunakan versi yang dikunci di `requirements.txt`.

## Langkah berikutnya yang mungkin
- Telegram signal alert
- session-aware filter London/New York
- import data MT5 yang lebih lengkap
- equity curve export
- parameter sweep / optimization
