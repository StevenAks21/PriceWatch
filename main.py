# main.py
from functions.getPrice import getPrice
from flask import Flask

app = Flask(__name__)


@app.route('/')
def home():
    return 'hi'


# Now call the function and store the result
current_price = getPrice("EUR/USD")

print(f"The current price is: {current_price}")

# Now you can use this for your alerts!
if float(current_price) > 1.0850:
    print("Price target hit! ")
