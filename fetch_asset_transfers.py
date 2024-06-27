import csv
from datetime import datetime

import requests
from web3 import Web3

from constants import data
from settings import Settings

settings = Settings()


def fetch_tx(chain: str, api_key: str, from_addr: str):
    base_url = f"https://{data[chain][0]}.g.alchemy.com/v2/{api_key}"

    payload = {
        "id": 1,
        "jsonrpc": "2.0",
        "method": "alchemy_getAssetTransfers",
        "params": [
            {
                "fromBlock": "0x0",
                "toBlock": "latest",
                "fromAddress": from_addr,
                "category": ["external", "erc20", "erc721", "erc1155"],
                "withMetadata": False,
                "excludeZeroValue": True
            }
        ]
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json"
    }

    response = requests.post(base_url, json=payload, headers=headers)
    parse_tx(chain, response.json())


def parse_tx(chain: str, res):
    with open('transactions.csv', 'w') as file:
        f_csv = csv.writer(file)

        headers = ['transaction_hash', 'timestamp', 'from', 'to', 'tokenType', 'value']
        f_csv.writerow(headers)

        w3 = Web3(Web3.HTTPProvider(data[chain][1]))

        for tx in res['result']['transfers']:
            block = w3.eth.get_block(tx['blockNum'])

            for tx_hash in block['transactions']:
                if w3.to_hex(tx_hash) == tx['hash']:

                    f_csv.writerow((tx['hash'],
                                    datetime.utcfromtimestamp(block['timestamp']).strftime("%b-%d-%Y %I:%M:%S %p %z"),
                                    tx['from'], tx['to'], tx['category'], tx['value']))


fetch_tx(settings.CHAIN, settings.API_KEY, settings.PB_ADDR)
