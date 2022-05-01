import alpaca_ccxt as ccxt
import env

# connect alpaca account
API_KEY = env.PAPER_API_KEY_ID
API_SECRET = env.PAPER_API_SECRET_KEY

alpaca = ccxt.alpaca(
  {
    "apikey": API_KEY,
    "secret": API_SECRET
  }
)

# enable sandboxmode
alpaca.setSandboxMode(True)

# access market data
def get_market_data():
  markets = alpaca.fetch_markets()
  return markets

# retrieve specific ticker data
def get_specific_ticker(specific_ticker):
  ticker = alpaca.fetch_ticker(specific_ticker)
  return ticker 

# retrieve ticker data with starting timestamp and data limit
def get_ticker_data(specific_ticker, since, limit):
  trades = alpaca.fetch_trades(specific_ticker, since, limit)
  return trades 

# retrieve account currency balance data
def get_acct_balances():
  balances = alpaca.fetch_balance()
  return balances

# create a new order
def new_order(specific_ticker, order_type, order_side, qty, price=None):
  if price:
    order = alpaca.create_order(specific_ticker, order_type, order_side, qty, price)
  else:
    order = alpaca.create_order(specific_ticker, order_type, order_side, qty, price)
  return order 

# access open orders
def open_orders():
  open_orders = alpaca.fetch_open_orders()
  return open_orders

# cancel order with order-id
def cancel_order(order_id):
  alpaca.cancel_order(order_id)


