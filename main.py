from requests import get
import time
import openai
from dotenv import load_dotenv
import os
import re

# Initial setup
load_dotenv()
APIKey = os.getenv("API_KEY")
openai.api_key = APIKey

currTime = time.ctime(time.time())

#Finding price of forex right now
url = 'https://www.investing.com/currencies/eur-usd-historical-data'
content = get(url).text
price = re.findall(r'data-test="instrument-price-last">([\d.]+)</div>', content)[0]

open('x.html', 'w', encoding='utf-8').write(content)


