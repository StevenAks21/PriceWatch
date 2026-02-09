from flask import Flask, jsonify, request
from functions.getPrice import getPrice
from functions.db import init_db, insert_user, check_password
import bcrypt
import sqlite3
import os
import dotenv
import jwt
from datetime import datetime, timedelta

dotenv.load_dotenv()
SECRET = os.getenv('SECRET').encode()
JWT_SECRET = os.getenv('JWT_SECRET', os.getenv('SECRET')).encode()

init_db()

app = Flask(__name__)

def verify_jwt_from_request():
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return None, (jsonify({"status": "failed", "message": "missing bearer token"}), 401)
    token = auth_header.split(" ", 1)[1].strip()
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        return payload, None
    except jwt.ExpiredSignatureError:
        return None, (jsonify({"status": "failed", "message": "token expired"}), 401)
    except jwt.InvalidTokenError:
        return None, (jsonify({"status": "failed", "message": "invalid token"}), 401)

@app.route('/api/register', methods = ['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password').encode()

    
    try:
        hashed = bcrypt.hashpw(password + SECRET, bcrypt.gensalt())
        insert_user(username, hashed)
    except sqlite3.IntegrityError:
        json = {"status" : "failed", 'message' : 'username already exists'}
        return jsonify(json), 400
        

    return jsonify({"status" :" success" , "message" : f'received data for {username}'}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password').encode()

    if check_password(username, password):
        payload = {
            "sub": username,
            "iat": datetime.utcnow(),
            "exp": datetime.utcnow() + timedelta(hours=12),
        }
        token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")
        return jsonify({"status": "success", "token": token}), 200
    else:
        return jsonify({"status": "failed", "message": "invalid credentials"}), 401

@app.route('/api/price', methods = ['GET'])
def get_price_json():
    _, error_response = verify_jwt_from_request()
    if error_response:
        return error_response
    symbol = request.args.get('symbol')
    print(symbol)
    if symbol == None:
        data = {
            "status" : 'Failed',
            "message" : 'Symbol is required!'
        }
        return jsonify(data), 400
    current_price = getPrice(symbol)
    data = {
        "status" : 'Success',
        "symbol": symbol,
        "price": float(current_price),
    }
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)
