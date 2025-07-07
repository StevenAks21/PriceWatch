from requests import get
import time
import openai
from dotenv import load_dotenv
import os

# Initial setup
load_dotenv()
APIKey = os.getenv("API_KEY")
openai.api_key = APIKey

currTime = time.ctime(time.time())

#Setting ChatGPT Up
print(get('https://www.investing.com/currencies/eur-usd-historical-data').text)
content = get('https://www.investing.com/currencies/eur-usd-historical-data').text

open('x.html', 'w', encoding='utf-8').write(content)
