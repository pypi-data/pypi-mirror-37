# coinbasepro-python
[![Build Status](https://travis-ci.org/yiwensong/coinbasepro-python.svg?branch=master)](https://travis-ci.org/yiwensong/coinbasepro-python)
[![Coverage Status](https://coveralls.io/repos/github/yiwensong/coinbasepro-python/badge.svg?branch=master)](https://coveralls.io/github/yiwensong/coinbasepro-python?branch=master)
[![Documentation Status](https://readthedocs.org/projects/cbpro2/badge/?version=master&style=flat)](https://cbpro2.readthedocs.io/en/master/)

The Python client for the [Coinbase Pro API](https://docs.pro.coinbase.com/) (formerly known as
the GDAX)

### Note
This is a fork of the original [cbpro project](https://github.com/danpaquin/coinbasepro-python).
I created this fork because between September and October of 2018, the maintainers of
that project seemed to be inactive in reviewing and merging pull requests. The goal of
this fork is as follows:
- Keep reasonably up-to-date with upstream
- Improve developer workflow and style
- Surface coverage stats to encourage unit testing

## Benefits
- A simple to use python wrapper for both public and authenticated endpoints.
- In about 10 minutes, you could be programmatically trading on one of the
largest Bitcoin exchanges in the *world*!
- Do not worry about handling the nuances of the API with easy-to-use methods
for every API endpoint.
- Gain an advantage in the market by getting under the hood of CB Pro to learn
what and who is behind every tick.

## Under Development
- Test Scripts
- Additional Functionality for the real-time order book
- FIX API Client **Looking for assistance**

## Getting Started
This README is documentation on the syntax of the python client presented in
this repository. See function docstrings for full syntax details.  
**This API attempts to present a clean interface to CB Pro, but in order to use it
to its full potential, you must familiarize yourself with the official CB Pro
documentation.**

- https://docs.pro.coinbase.com/

- You may manually install the project or use ```pip```:
```python
pip install cbpro2
#or
pip install git+git://github.com/yiwensong/coinbasepro-python.git
```

### Public Client
Only some endpoints in the API are available to everyone.  The public endpoints
can be reached using ```PublicClient```

```python
import cbpro
public_client = cbpro.PublicClient()
```

### PublicClient Methods
- [get_products](https://docs.pro.coinbase.com//#get-products)
```python
public_client.get_products()
```

- [get_product_order_book](https://docs.pro.coinbase.com/#get-product-order-book)
```python
# Get the order book at the default level.
public_client.get_product_order_book('BTC-USD')
# Get the order book at a specific level.
public_client.get_product_order_book('BTC-USD', level=1)
```

- [get_product_ticker](https://docs.pro.coinbase.com/#get-product-ticker)
```python
# Get the product ticker for a specific product.
public_client.get_product_ticker(product_id='ETH-USD')
```

- [get_product_trades](https://docs.pro.coinbase.com/#get-trades) (paginated)
```python
# Get the product trades for a specific product.
# Returns a generator
public_client.get_product_trades(product_id='ETH-USD')
```

- [get_product_historic_rates](https://docs.pro.coinbase.com/#get-historic-rates)
```python
public_client.get_product_historic_rates('ETH-USD')
# To include other parameters, see function docstring:
public_client.get_product_historic_rates('ETH-USD', granularity=3000)
```

- [get_product_24hr_stats](https://docs.pro.coinbase.com/#get-24hr-stats)
```python
public_client.get_product_24hr_stats('ETH-USD')
```

- [get_currencies](https://docs.pro.coinbase.com/#get-currencies)
```python
public_client.get_currencies()
```

- [get_time](https://docs.pro.coinbase.com/#time)
```python
public_client.get_time()
```

### Authenticated Client

Not all API endpoints are available to everyone.
Those requiring user authentication can be reached using `AuthenticatedClient`.
You must setup API access within your
[account settings](https://www.pro.coinbase.com/settings/api).
The `AuthenticatedClient` inherits all methods from the `PublicClient`
class, so you will only need to initialize one if you are planning to
integrate both into your script.

```python
import cbpro
auth_client = cbpro.AuthenticatedClient(key, b64secret, passphrase)
# Use the sandbox API (requires a different set of API access credentials)
auth_client = cbpro.AuthenticatedClient(key, b64secret, passphrase,
                                  api_url="https://api-public.sandbox.pro.coinbase.com")
```

### Pagination
Some calls are [paginated](https://docs.pro.coinbase.com/#pagination), meaning multiple
calls must be made to receive the full set of data. The CB Pro Python API provides
an abstraction for paginated endpoints in the form of generators which provide a
clean interface for iteration but may make multiple HTTP requests behind the
scenes. The pagination options `before`, `after`, and `limit` may be supplied as
keyword arguments if desired, but aren't necessary for typical use cases.
```python
fills_gen = auth_client.get_fills()
# Get all fills (will possibly make multiple HTTP requests)
all_fills = list(fills_gen)
```
One use case for pagination parameters worth pointing out is retrieving only
new data since the previous request. For the case of `get_fills()`, the
`trade_id` is the parameter used for indexing. By passing
`before=some_trade_id`, only fills more recent than that `trade_id` will be
returned. Note that when using `before`, a maximum of 100 entries will be
returned - this is a limitation of CB Pro.
```python
from itertools import islice
# Get 5 most recent fills
recent_fills = islice(auth_client.get_fills(), 5)
# Only fetch new fills since last call by utilizing `before` parameter.
new_fills = auth_client.get_fills(before=recent_fills[0]['trade_id'])
```

### AuthenticatedClient Methods
- [get_accounts](https://docs.pro.coinbase.com/#list-accounts)
```python
auth_client.get_accounts()
```

- [get_account](https://docs.pro.coinbase.com/#get-an-account)
```python
auth_client.get_account("7d0f7d8e-dd34-4d9c-a846-06f431c381ba")
```

- [get_account_history](https://docs.pro.coinbase.com/#get-account-history) (paginated)
```python
# Returns generator:
auth_client.get_account_history("7d0f7d8e-dd34-4d9c-a846-06f431c381ba")
```

- [get_account_holds](https://docs.pro.coinbase.com/#get-holds) (paginated)
```python
# Returns generator:
auth_client.get_account_holds("7d0f7d8e-dd34-4d9c-a846-06f431c381ba")
```

- [buy & sell](https://docs.pro.coinbase.com/#place-a-new-order)
```python
# Buy 0.01 BTC @ 100 USD
auth_client.buy(price='100.00', #USD
               size='0.01', #BTC
               order_type='limit',
               product_id='BTC-USD')
```
```python
# Sell 0.01 BTC @ 200 USD
auth_client.sell(price='200.00', #USD
                size='0.01', #BTC
                order_type='limit',
                product_id='BTC-USD')
```
```python
# Limit order-specific method
auth_client.place_limit_order(product_id='BTC-USD',
                              side='buy',
                              price='200.00',
                              size='0.01')
```
```python
# Place a market order by specifying amount of USD to use.
# Alternatively, `size` could be used to specify quantity in BTC amount.
auth_client.place_market_order(product_id='BTC-USD',
                               side='buy',
                               funds='100.00')
```
```python
# Stop order. `funds` can be used instead of `size` here.
auth_client.place_stop_order(product_id='BTC-USD',
                              side='buy',
                              price='200.00',
                              size='0.01')
```

- [cancel_order](https://docs.pro.coinbase.com/#cancel-an-order)
```python
auth_client.cancel_order("d50ec984-77a8-460a-b958-66f114b0de9b")
```
- [cancel_all](https://docs.pro.coinbase.com/#cancel-all)
```python
auth_client.cancel_all(product_id='BTC-USD')
```

- [get_orders](https://docs.pro.coinbase.com/#list-orders) (paginated)
```python
# Returns generator:
auth_client.get_orders()
```

- [get_order](https://docs.pro.coinbase.com/#get-an-order)
```python
auth_client.get_order("d50ec984-77a8-460a-b958-66f114b0de9b")
```

- [get_fills](https://docs.pro.coinbase.com/#list-fills) (paginated)
```python
# All return generators
auth_client.get_fills()
# Get fills for a specific order
auth_client.get_fills(order_id="d50ec984-77a8-460a-b958-66f114b0de9b")
# Get fills for a specific product
auth_client.get_fills(product_id="ETH-BTC")
```

- [deposit & withdraw](https://docs.pro.coinbase.com/#depositwithdraw)
```python
depositParams = {
        'amount': '25.00', # Currency determined by account specified
        'coinbase_account_id': '60680c98bfe96c2601f27e9c'
}
auth_client.deposit(depositParams)
```
```python
# Withdraw from CB Pro into Coinbase Wallet
withdrawParams = {
        'amount': '1.00', # Currency determined by account specified
        'coinbase_account_id': '536a541fa9393bb3c7000023'
}
auth_client.withdraw(withdrawParams)
```

### WebsocketClient
If you would like to receive real-time market updates, you must subscribe to the
[websocket feed](https://docs.pro.coinbase.com/#websocket-feed).

#### Subscribe to a single product
```python
import cbpro
# Paramters are optional
wsClient = cbpro.WebsocketClient(url="wss://ws-feed.pro.coinbase.com", products="BTC-USD")
# Do other stuff...
wsClient.close()
```

#### Subscribe to multiple products
```python
import cbpro
# Paramaters are optional
wsClient = cbpro.WebsocketClient(url="wss://ws-feed.pro.coinbase.com",
                                products=["BTC-USD", "ETH-USD"])
# Do other stuff...
wsClient.close()
```

### WebsocketClient + Mongodb
The ```WebsocketClient``` now supports data gathering via MongoDB. Given a
MongoDB collection, the ```WebsocketClient``` will stream results directly into
the database collection.
```python
# import PyMongo and connect to a local, running Mongo instance
from pymongo import MongoClient
import cbpro
mongo_client = MongoClient('mongodb://localhost:27017/')

# specify the database and collection
db = mongo_client.cryptocurrency_database
BTC_collection = db.BTC_collection

# instantiate a WebsocketClient instance, with a Mongo collection as a parameter
wsClient = cbpro.WebsocketClient(url="wss://ws-feed.pro.coinbase.com", products="BTC-USD",
    mongo_collection=BTC_collection, should_print=False)
wsClient.start()
```

### WebsocketClient Methods
The ```WebsocketClient``` subscribes in a separate thread upon initialization.
There are three methods which you could overwrite (before initialization) so it
can react to the data streaming in.  The current client is a template used for
illustration purposes only.

- onOpen - called once, *immediately before* the socket connection is made, this
is where you want to add initial parameters.
- onMessage - called once for every message that arrives and accepts one
argument that contains the message of dict type.
- on_close - called once after the websocket has been closed.
- close - call this method to close the websocket connection (do not overwrite).
```python
import cbpro, time
class myWebsocketClient(cbpro.WebsocketClient):
    def on_open(self):
        self.url = "wss://ws-feed.pro.coinbase.com/"
        self.products = ["LTC-USD"]
        self.message_count = 0
        print("Lets count the messages!")
    def on_message(self, msg):
        self.message_count += 1
        if 'price' in msg and 'type' in msg:
            print ("Message type:", msg["type"],
                   "\t@ {:.3f}".format(float(msg["price"])))
    def on_close(self):
        print("-- Goodbye! --")

wsClient = myWebsocketClient()
wsClient.start()
print(wsClient.url, wsClient.products)
while (wsClient.message_count < 500):
    print ("\nmessage_count =", "{} \n".format(wsClient.message_count))
    time.sleep(1)
wsClient.close()
```

### Real-time OrderBook
The ```OrderBook``` subscribes to a websocket and keeps a real-time record of
the orderbook for the product_id input.  Please provide your feedback for future
improvements.

```python
import cbpro, time
order_book = cbpro.OrderBook(product_id='BTC-USD')
order_book.start()
time.sleep(10)
order_book.close()
```

## Development

### Development Environment
A development environment can be created and activated with the commands
```bash
make venv && . venv/bin/activate
```

### Automated Testing
Unit test framework uses pytest, coverage, and tox. A test suite is under development,
please contribute to the coverage. Tests for the authenticated client require a
set of sandbox API credentials. To provide them, rename
`api_config.json.example` in the tests folder to `api_config.json` and edit the
file accordingly. To run the tests, start in the project directory and run

```bash
make test
```

### Pre-commit
This project uses pre-commit to enforce coding style. You can run pre-commit with
the following command (after activating the venv)
```bash
pre-commit run --files [FILES]
```
You can also run
```bash
pre-commit run --all-files
```
but that is guaranteed to fail because of legacy code that has yet to be linted.
