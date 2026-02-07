from flask import Flask, jsonify
from functions.getPrice import getPrice

app = Flask(__name__)

@app.route('/api/price')
def get_price_json():
    current_price = getPrice("EUR/USD")
    data = {
        "symbol": "EUR/USD",
        "price": float(current_price),
        "target_hit": float(current_price) > 1.0850,
        "unit": "USD"
    }
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)