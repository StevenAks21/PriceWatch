from requests import get
import time
import openai
from dotenv import load_dotenv
import os
import re
import base64
from functions import screenshot_chart


# Initial setup
load_dotenv()
APIKey = os.getenv("API_KEY")
openai.api_key = APIKey
Bot = openai.OpenAI(api_key=APIKey)

currTime = time.ctime(time.time())

#Finding price of forex right now
url = 'https://www.investing.com/currencies/eur-usd-historical-data'
content = get(url).text
price = float(re.findall(r'data-test="instrument-price-last">([\d.]+)</div>', content)[0])


#Ask for AI Opinion
screenshot_chart.screenshot_chart()
image_path = 'eurusd_2025-07-07_18-04.png'
with open(image_path, 'rb') as image_file:
    image_bytes = image_file.read()
    base64image = base64.b64encode(image_bytes).decode('utf-8')

response = Bot.responses.create(model= 'gpt-4.1', input =
[
    {
        "role" : "user",
        "content" : 
        [
            {'type' : 'input_text', 'text' : 'hi, what do you see on the image? whats your prediciton'},
            {'type' : 'input_image', 'image_url' : f'data:image/png;base64,{base64image}'}
        ]
    }
])
print(response.output_text)
open('x.html', 'w', encoding='utf-8').write(content)
