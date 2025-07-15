#Finding price of forex right now
from requests import get
import re
def getPrice():
    url = 'https://www.investing.com/currencies/eur-usd-historical-data'
    content = get(url).text
    price = float(re.findall(r'data-test="instrument-price-last">([\d.]+)</div>', content)[0])
    return price