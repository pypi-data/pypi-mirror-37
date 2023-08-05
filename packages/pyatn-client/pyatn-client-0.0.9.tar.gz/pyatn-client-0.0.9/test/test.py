#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyatn_client import Atn

#  atn = Atn(
#      http_provider='https://rpc-test.atnio.net',   # or use offical default one: https://rpc-test.atnio.net
#      pk_file='./dbot-examples/accounts/signer02/keystore/UTC--2018-06-19T08-46-10.312652809Z--0cc1f6e1a55b163301434a47b1cb68cbd7e27cad',
#      pw_file='./dbot-examples/accounts/signer02/password/passwd'
#  )
#
#  response = atn.call_dbot_api(dbot_address='0xfd4F504F373f0af5Ff36D9fbe1050E6300699230',
#                               uri='/reg',
#                               method='POST',
#                               data={'theme': '中秋月更圆'})
#  print(response)
#
DBOTADDRESS = '0xfd4F504F373f0af5Ff36D9fbe1050E6300699230' # address of the DBot you want to test, use 'AI poetry' as example
URI = '/reg'        # uri of the DBot's API endpoint which you want to call
METHOD = 'POST'     # method of the DBot's API endpoint which you want to call
requests_kwargs = {
    "data": {
        "theme": "中秋月更圆"
    }
}

# init Atn
atn = Atn(
    pk_file='./dbot-examples/accounts/signer02/keystore/UTC--2018-06-19T08-46-10.312652809Z--0cc1f6e1a55b163301434a47b1cb68cbd7e27cad',
    pw_file='./dbot-examples/accounts/signer02/password/passwd'
)

# Call a DBot API 12 times
for i in range(12):
    response = atn.call_dbot_api(dbot_address=DBOTADDRESS,
                                uri=URI,
                                method=METHOD,
                                **requests_kwargs)
    print('Call {}:\n{}'.format(i + 1, response.text))

# close the channel only when you do not need it any more,
# the remain balance in the channel will be returned to your account
atn.close_channel(DBOTADDRESS)

#  DBOTADDRESS = '0xfd4F504F373f0af5Ff36D9fbe1050E6300699230' # address of the DBot you want to test
#  URI = '/reg'        # uri of the DBot's API endpoint which you want to call
#  METHOD = 'POST'     # method of the DBot's API endpoint which you want to call
#  requests_kwargs = {
#      "data": {
#          "theme": "中秋月更圆"
#      }
#  }
#
#  # get price of the endpoint to be called
#  price = atn.get_price(DBOTADDRESS, URI, METHOD)
#  # open channel with the DBot, only one opened channel is allowed between two address
#  # it will return the channel if one existed.
#  channel = atn.open_channel(DBOTADDRESS, 10 * price)
#  # wait DBot server sync channel info with the blockchain
#  atn.wait_dbot_sync(DBOTADDRESS)
#  if channel.deposit - channel.balance < price:
#      atn.topup_channel(DBOTADDRESS, 10 * price)
#      # wait DBot server sync channel info with the blockchain
#      atn.wait_dbot_sync(DBOTADDRESS)
#
#  call_count = 1
#  while call_count <= 12:
#      print('Call {}:'.format(call_count))
#      response = atn.call_dbot_api(dbot_address=DBOTADDRESS,
#                                  uri=URI,
#                                  method=METHOD,
#                                  **requests_kwargs)
#      call_count += 1
#      print(response.text)
#
#  # close the channel only when you do not need it any more,
#  # the remain balance in the channel will be returned to your account
#  atn.close_channel(DBOTADDRESS)
#
