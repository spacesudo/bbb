import requests
from dotenv import load_dotenv
import os
import asyncio
from TonTools import *
#MNEMONICS, JETTON_MASTER, amount, dest_addr

load_dotenv()

KEY = os.getenv('BRIDGE_API')

import requests
import json

def exchange(from_curr,from_net, to_net , to_curr, amount, address):
  url = "https://api.changenow.io/v2/exchange"

  payload = json.dumps({
    "fromCurrency": from_curr,
    "toCurrency": to_curr,
    "fromNetwork": from_net,
    "toNetwork": to_net,
    "fromAmount": amount,
    "toAmount": "",
    "address": address,
    "extraId": "",
    "refundAddress": '',
    "refundExtraId": "",
    "userId": "",
    "payload": "",
    "contactEmail": "",
    "source": "",
    "flow": "standard",
    "type": "direct",
    "rateId": ""
})
  headers = {
    'Content-Type': 'application/json',
    'x-changenow-api-key': KEY
  }

  response = requests.request("POST", url, headers=headers, data=payload)
  return response.json()


async def transfer_jet(dest: str, jetton_addr: str, mnemonics: list, amount: float):
    client = TonCenterClient(orbs_access=True)
    your_wallet = Wallet(provider=client, mnemonics=mnemonics, version='v3r2')
    """jet = 'EQC4FtSgVLwP6USbYXsVgTZ3hNlY_Rl5SHRWjmTUWa1K2oIe'
    j = Jetton(jet, provider=client).address
    print(j)"""
    await your_wallet.transfer_jetton_by_jetton_wallet(
        destination_address= dest,
        jetton_wallet=jetton_addr, 
        jettons_amount= amount,
    )

    print('done')



def minimum(from_curr, from_net, to_net , to_curr):

  url = f"https://api.changenow.io/v2/exchange/min-amount?fromCurrency={from_curr}&toCurrency={to_curr}&fromNetwork={from_net}&toNetwork={to_net}&flow=standard"

  payload={}
  headers = {
    'x-changenow-api-key': KEY
  }

  response = requests.request("GET", url, headers=headers, data=payload)
  return response.json()['minAmount']


def exchange_status(tx_id):
  url = f"https://api.changenow.io/v2/exchange/by-id?id={tx_id}"

  payload={}
  headers = {
    'x-changenow-api-key': KEY
  }

  response = requests.request("GET", url, headers=headers, data=payload)
  return response.json()

def output(from_curr,from_net, to_net , to_curr, amount):
    url = f"https://api.changenow.io/v2/exchange/estimated-amount?fromCurrency={from_curr}&toCurrency={to_curr}&fromAmount={amount}&toAmount=&fromNetwork={from_net}&toNetwork={to_net}&flow=fixed-rate&type=&useRateId=true"

    payload={}
    headers = {
      'x-changenow-api-key': KEY
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    return response.json()['toAmount']





if __name__ == "__main__":
  x = exchange('usdt','trx','ton','ton',10,"UQDLzebYWhJaIt5YbZ5vz_glIbfqP7PxNg9V54HW3jSIhDPe")
  print(x)
  