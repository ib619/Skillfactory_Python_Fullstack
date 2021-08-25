import requests
import json
from config import keys, API_KEY


class APIException(Exception):
    pass


class CryptoConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str) -> float:
        try:
            quote_ticker = keys[quote.casefold()]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту: {quote}')

        try:
            base_ticker = keys[base.casefold()]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту: {base}')

        r = requests.get(f'http://api.exchangeratesapi.io/v1/latest?access_key={API_KEY}cad2b&symbols={base_ticker},{quote_ticker}')

        total_base = json.loads(r.content)['rates'][keys[base.casefold()]]
        total_quote = json.loads(r.content)['rates'][keys[quote.casefold()]]
        data = total_base/total_quote
        total_base_scaled = float(data) * float(amount)

        return round(total_base_scaled, 4)


