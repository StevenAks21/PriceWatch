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
BotResponse = openai.responses.create(
    model = 'gpt-4.1',
    input = f'hi, guess whgere im from, its now exactly {currTime}'
)

print(BotResponse.output_text)
print(currTime)