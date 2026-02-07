from dotenv import load_dotenv
import os
from twelvedata import TDClient

load_dotenv()
api_key = os.getenv('API_KEY')
print(api_key)

td = TDClient(api_key)

