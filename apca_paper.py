from ast import Str, Try
import time
import alpaca_trade_api as api
import random
import pandas as pd
import env

API_KEY = env.PAPER_API_KEY_ID
API_SECRET = env.PAPER_API_SECRET_KEY
BASE_URL = env.PAPER_API_ENDPOINT

# instantiate rest api connection
alpaca = api.REST(API_KEY, API_SECRET, BASE_URL)

# Fetch 1Minutes historical bars of Bitcoin
def get_bars(ticker: Str):
  bars = alpaca.get_crypto_bars(ticker, api.TimeFrame.Minute).df
  #print(bars)
  return bars

def get_bars_by_exchange(ticker: str, exchange: str):
  """filter data by exchange

  Args:
      ticker (str): cryptocurrency ticker pair
      exchange (str): cyptocurrency exchange platform (ex. coinbase)
  """
  bars = get_bars(ticker)
  filtered_bars = bars[bars.exchange == exchange]
  print(filtered_bars)
  return filtered_bars

def create_market_order(ticker: str,
                        qty: float,
                        side: str,
                        type: str = "market",
                        time_in_force: str = "day",
                        limit_price: str = None,
                        stop_price: str = None,
                        client_order_id: str = None,
                        extended_hours: bool = None,
                        order_class: str = None,
                        take_profit: dict = None,
                        stop_loss: dict = None,
                        trail_price: str = None,
                        trail_percent: str = None,
                        notional: float = None
                        ):
  order = alpaca.submit_order(ticker, qty, side, type, time_in_force, limit_price,
                           stop_price, client_order_id, extended_hours, order_class,
                           take_profit, stop_loss, trail_price, trail_percent, notional)
  print(order)
  return order 


def get_crypto_position(ticker: str):
  """Get current position on a ticker. 
     Yields error if no position is held

  Args:
      ticker (str): cryptocurrency ticker

  Returns:
      _type_: _description_
  """
  try:
    position = alpaca.get_position(ticker)
    print(position)
    return position
  except api.rest.APIError:
    print(f"\n------\nposition does not exist\n-----\n")
  except Exception as err:
    print(f"\n-----\n{err}\n-----\n")

def get_all_positions(filter: str = None):
  positions = alpaca.list_positions()

  if filter:
    position_qty = 0
    for position in positions:
      if position.symbol == filter:
        position_qty = float(position.qty)
    print(f"\n-----\n{filter}: {position_qty}\n-----\n")
    return position_qty

  print(positions)
  return positions

def make_trade_decision(ticker: str, position: float, decision: bool, qty: float = 1):
  # CHECK IF WE SHOULD BUY
  if (position == 0) and (decision == True):
    # we buy one crypto
    print("The gods have spoken")
    print(f'Symbol: {ticker}  \nSide: BUY  \nQuantity: {qty}')

    # submit market order
    create_market_order(ticker, qty=1, side='buy')
  # CHECK IS WE SHOULD SELL
  elif (position > 0) and (decision == False):
    # we sell one cryto
    print('The gods have spoken')
    print(f'Symbol: {ticker} \nSide: SELL \nQuantity: {qty}')
      
    # submit market order
    create_market_order(ticker, qty=qty, side='sell')


def coin_flip_trade(ticker: str):
  SYMBOL: str = ticker 

  while True:
    # get current position
    position = get_all_positions(SYMBOL)

    # randomly check if buy or sell
    gods_say_buy = random.choice([True, False])
    print(f'\nHolding: {SYMBOL} = {position} \nGods: {gods_say_buy}')

    # make decision to buy or sell based on information provided.
    make_trade_decision(ticker=SYMBOL, position=position, decision=gods_say_buy)

    print(f'\n-------\nLets wait for the gods to manifest again\n-----\n')
    print("*"*20)
    time.sleep(10)



def process_crypto_iter(iter):
  """process get_crytpo_trade_iter()
     results.
  """
  for item in iter:
    print(f"\n-----\n{item}\n-----\n")


if __name__ == "__main__":
  #print(alpaca.get_asset("BTCUSD"))
  #get_bars_by_exchange("BTCUSD", "CBSE")
  #create_market_order("BTCUSD", qty=1, side='sell')
  #get_crypto_position("BTCUSD")
  #get_all_positions()
  coin_flip_trade('BTCUSD')
  print(f'-----\ndone\n-----')
