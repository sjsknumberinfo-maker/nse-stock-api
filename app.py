from flask import Flask, jsonify
from flask_cors import CORS
import yfinance as yf

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return jsonify({"status": "NSE Stock Scanner API is running"})

@app.route('/stock/<symbol>')
def get_stock(symbol):
    try:
        ticker = yf.Ticker(f"{symbol}.NS")
        hist = ticker.history(period="1y", interval="1d")

        if hist.empty:
            return jsonify({"error": f"No data found for {symbol}"}), 404

        data = []
        for date, row in hist.iterrows():
            data.append({
                "date": str(date.date()),
                "o": round(float(row["Open"]), 2),
                "h": round(float(row["High"]), 2),
                "l": round(float(row["Low"]), 2),
                "c": round(float(row["Close"]), 2),
                "v": int(row["Volume"])
            })

        return jsonify({"symbol": symbol, "data": data})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
