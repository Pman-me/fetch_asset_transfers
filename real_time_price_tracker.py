import os.path
import threading
import time
from datetime import datetime

import requests
import csv
from settings import Settings


def price_tracker(url: str, token_addr: str):
    headers = {
        "accept": "application/json",
        "content-type": "application/json"
    }
    if not os.path.exists('price_tracker.csv'):
        with open('price_tracker.csv', 'w') as file:
            f_csv = csv.writer(file)
            headers = ['Token', 'date', 'price', 'volume 24h']
            f_csv.writerow(headers)

    with open('price_tracker.csv', 'a') as file:
        try:
            data = requests.get(url + token_addr, headers=headers).json()['pairs'][0]

            f_csv = csv.writer(file)
            f_csv.writerow((data['baseToken']['symbol'], datetime.now(), data['priceUsd'], data['volume']['h24']))
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)


def run_threaded(func, *args):
    job = threading.Thread(target=func, args=args)
    job.start()


while True:
    run_threaded(price_tracker, Settings().PRICE_TRACKER_API_URL, '0xba5e6fa2f33f3955f0cef50c63dcc84861eab663')
    time.sleep(20)
