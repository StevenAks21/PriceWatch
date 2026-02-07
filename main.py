from flask import Flask, jsonify, request
from functions.getPrice import getPrice
from functions.db import init_db, check_unique_user, insert_user
import bcrypt
import sqlite3

init_db()

app = Flask(__name__)

@app.route('/api/register', methods = ['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    try:
        insert_user(username, password)
    except sqlite3.IntegrityError:
        json = {"status" : "failed", 'message' : 'username already exists'}
        return jsonify(json), 400

    return jsonify({"status" :" success" , "message" : f'received data for {username}'}), 201

@app.route('/api/login', methods = ['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    

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