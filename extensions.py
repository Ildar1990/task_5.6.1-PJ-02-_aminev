import json
import requests
from config import keys


class APIException(Exception):
    pass


class Converter:
    @staticmethod
    def get_price(base, quote, amount):

        try:
            base_cur = keys[base]
            quote_cur = keys[quote]
        except KeyError as e:
            raise APIException(f'вы ввели неправильную или несуществующую валюту: {e}')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'вы неправильно ввели количество конвертируемой валюты.')

        r = requests.get(f'https://v6.exchangerate-api.com/v6/4f5f15561ccade4278ec970c/pair/{base_cur}/{quote_cur}')
        rate = json.loads(r.content)['conversion_rate']
        return amount * rate
