import os
import dateutil.parser
from coinbase.wallet.client import Client as CoinbaseClient

# export your coinbase_api_key and coinbase_api_secret as environmental vars for now. Probably will be oath2 when this is a web app
coinbase_api_key = os.environ.get('coinbase_api_key')
coinbase_api_secret = os.environ.get('coinbase_api_secret')

cbclient = CoinbaseClient(coinbase_api_key, coinbase_api_secret)

print "Your coinbase accounts:"
cbaccounts = cbclient.get_accounts()
for account in cbaccounts["data"]:
    print "# %s: %s %s" % ( account["name"], account["balance"]["amount"], account["balance"]["currency"] )
    print "# Coinbase %s transactions #" % account["name"]
    cbtransactions = cbclient.get_transactions(account['id'])
    if account["balance"]["currency"] != "USD":
        for tx in cbtransactions["data"]:
            txdate = dateutil.parser.parse(tx["created_at"]).date()
            marketinfo = cbclient.get_spot_price(currency_pair = tx["amount"]["currency"]+'-USD', date = txdate )
            # print "The price for %s-USD on %s was: %s" % ( tx["amount"]["currency"], txdate, marketinfo["amount"] )
            print "%s: %s %s (%s @ %s USD %s)" % (tx["created_at"], tx["amount"]["amount"], tx["amount"]["currency"], tx["details"]["title"], marketinfo["amount"], tx["details"]["subtitle"] )
        print ""
