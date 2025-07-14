from requests import get
import time
import openai
from dotenv import load_dotenv
import os

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
response = Bot.responses.create(model= 'gpt-4.1', input='hi!, say something in indonesian')
print(response.output_text)
open('x.html', 'w', encoding='utf-8').write(content)
