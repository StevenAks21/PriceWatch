import os
from dotenv import load_dotenv
from twelvedata import TDClient

load_dotenv()
api_key = os.getenv('API_KEY')
td = TDClient(apikey=api_key)

def getPrice(symbol):
    try:
        price_data = td.price(symbol=symbol).as_json()
        return price_data['price']
    except Exception as e:
        return f"Error: {e}"