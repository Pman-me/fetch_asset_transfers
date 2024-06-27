import requests

from settings import Settings


settings = Settings()
base_url = f'https://{settings.CHAIN}.g.alchemy.com/v2/{settings.API_KEY}'


def get_token_metadata(token_addr: str, base_url):
    payload = {
        "id": 1,
        "jsonrpc": "2.0",
        "method": "alchemy_getTokenMetadata",
        "params": [token_addr]
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json"
    }

    return requests.post(base_url, json=payload, headers=headers)


def get_token_balances(eoa_addr: str, base_url):
    payload = {
        "id": 1,
        "jsonrpc": "2.0",
        "method": "alchemy_getTokenBalances",
        "params": [eoa_addr, "erc20"]
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json"
    }

    response = requests.post(base_url, json=payload, headers=headers).json()['result']

    for i, token in enumerate(filter(
            lambda x: x['tokenBalance'] != '0x0000000000000000000000000000000000000000000000000000000000000000',
            response['tokenBalances']), start=1):

        metadata = get_token_metadata(token['contractAddress'], base_url).json()['result']
        print(f"{i}. {metadata['name']}: {token['tokenBalance']} {metadata['symbol']}")


def get_nfts_for_owner(eoa_addr: str, base_url):
    url = f"{base_url}/getNFTsForOwner?owner={eoa_addr}&withMetadata=true&pageSize=100"

    headers = {"accept": "application/json"}
    nfts = requests.get(url, headers=headers).json()['ownedNfts']
    for i, nft in enumerate(nfts, start=1):
        balance = nft['balance']
        metadata = nft['contractMetadata']
        name = metadata['name']
        token_type = metadata['tokenType']
        if 'symbol' in metadata.keys():
            symbol = metadata['symbol']
            print(f"{i}. name: {name}\tbalance: {balance}\tsymbol: {symbol}\ttoken Type: {token_type}")
        else:
            print(f"{i}. name: {name}\tbalance: {balance}\ttoken Type: {token_type}")


get_token_balances(settings.PB_ADDR, base_url)
get_nfts_for_owner(settings.PB_ADDR, base_url)
