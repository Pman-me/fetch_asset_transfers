import csv
from datetime import datetime
from pprint import pprint

import requests
from web3 import Web3
from web3.middleware import geth_poa_middleware

from constants import chain_rpc_map
from settings import Settings

settings = Settings()


def fetch_tx(chain: str, api_key: str, from_addr: str = None, to_addr: str = None):
    base_url = f"https://{chain_rpc_map[chain][0]}.g.alchemy.com/v2/{api_key}"

    payload = {
        "id": 1,
        "jsonrpc": "2.0",
        "method": "alchemy_getAssetTransfers",
        "params": [
            {
                "fromBlock": "0x0",
                "category": ["erc20"],
                "contractAddresses": ["0x4ed4E862860beD51a9570b96d89aF5E1B0Efefed"],
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
    parse_tx(chain, response.json(), from_addr, to_addr)


def parse_tx(chain: str, res, from_addr: str = None, to_addr: str = None):
    with open('transfers.csv', 'w') as file:
        f_csv = csv.writer(file)

        headers = ['transaction_hash', 'timestamp', 'from', 'to', 'tokenType', 'value']
        f_csv.writerow(headers)

        w3 = Web3(Web3.HTTPProvider(chain_rpc_map[chain][1]))
        w3.middleware_onion.inject(geth_poa_middleware, layer=0)

        for response_tx in res['result']['transfers']:
            if response_tx['to'] == '0x9f07f8a82cb1af1466252e505b7b7ddee103bc91' or response_tx['from'] == '0x9f07f8a82cb1af1466252e505b7b7ddee103bc91':

                block = w3.eth.get_block(response_tx['blockNum'])
                for tx_hash in block['transactions']:
                    if w3.to_hex(tx_hash) == response_tx['hash']:

                        f_csv.writerow((response_tx['hash'],
                                        datetime.utcfromtimestamp(block['timestamp']).strftime("%b-%d-%Y %I:%M:%S %p %z"),
                                        response_tx['from'], response_tx['to'], response_tx['value']))


fetch_tx(settings.CHAIN, settings.API_KEY, settings.PB_ADDR)
