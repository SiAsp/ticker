import sys
import os
import requests
import threading
import time
import json

if len(sys.argv) < 2:
    print('Please enter some coins to track')
    exit()


def get_price(coin):
    while True:
        url = 'https://api.bitfinex.com/v1/pubticker/{}{}'
        first_coin = 'USD' if coin == 'BTC' else 'BTC'
        r = requests.get(url.format(coin, first_coin))
        if r.status_code == 200:
            r = r.json()
            new_price = float(r['last_price'])
            coins[coin][1] = (new_price - coins[coin][0]) / coins[coin][0] * 100 if coins[coin][0] != 0 else 0  # Calculate price change in percent
            coins[coin][0] = new_price
        else:
            print(r.status_code, '\n', r.text)
        time.sleep(10)


coins = {'BTC': [0, 0]}
for coin in sys.argv[1:]:
    coins[coin.upper()] = [0, 0]

for coin, price in coins.items():
    t = threading.Thread(target=get_price, args=(coin,))
    t.start()

while True:
    os.system('clear')
    for coin, data in coins.items():
        if coin != 'BTC':
            print('{}: BTC {:.8f} ${:.5f} ({}%)'.format(coin, data[0], data[0] * coins['BTC'][0], data[1]))
        else:
            print('{}: ${:.2f} ({}%)'.format(coin, data[0], data[1]))

    time.sleep(0.5)
