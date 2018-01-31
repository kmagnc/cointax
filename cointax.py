import os
from tabulate import tabulate
import dateutil.parser
from coinbase.wallet.client import Client as CoinbaseClient

# TODO: pip install list / file (coinbase, python-binance, tabulate)

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
        tableList = []
        for tx in cbtransactions["data"]:
            txdate = dateutil.parser.parse(tx["created_at"]).date()
            marketinfo = cbclient.get_spot_price(currency_pair = tx["amount"]["currency"]+'-USD', date = txdate )
            tableList.append( [ txdate, tx["type"], tx["amount"]["amount"], tx["amount"]["currency"], marketinfo["amount"], float(marketinfo["amount"])*float(tx["amount"]["amount"]), tx["details"]["title"]+" "+tx["details"]["subtitle"] ])
            # print "The price for %s-USD on %s was: %s" % ( tx["amount"]["currency"], txdate, marketinfo["amount"] )
            # print "%s %s %s %s @ $%s MV (Worth $%s)\t\t(%s %s)" % (txdate, tx["type"], tx["amount"]["amount"], tx["amount"]["currency"], marketinfo["amount"], float(marketinfo["amount"])*float(tx["amount"]["amount"]), tx["details"]["title"], tx["details"]["subtitle"] )
            # print tabulate([[ txdate, tx["type"], tx["amount"]["amount"], tx["amount"]["currency"], marketinfo["amount"], float(marketinfo["amount"])*float(tx["amount"]["amount"]), tx["details"]["title"], tx["details"]["subtitle"] ]], headers=['Date', 'Tx Type', 'Qty', 'Cur', 'Market', 'Ttl', 'Description', '2D'])
        print tabulate( tableList, headers=['Date', 'Tx Type', 'Qty', 'Cur', 'Mkt Rate', 'Tx Value', 'Description'])
        print ""
