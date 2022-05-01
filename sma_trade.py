import apca_paper as apca
from datetime import datetime, timedelta
import math
import time

SYMBOL = 'BTCUSD'
SMA_FAST = 12
SMA_SLOW = 24
QTY_PER_TRADE = 1

def get_pause():
  now = datetime.now()
  print(f'\nnow: {now}\n')
  next_min = now.replace(second=0, microsecond=0) + timedelta(minutes=1)
  print(f'\nnext minute: {next_min}\n')
  pause = math.ceil((next_min - now).seconds)
  print(f"\nsleep for {pause}\n")
  return pause 

# return a series with the moving average
def get_sma(series, periods):
  return series.rolling(periods).mean()

# check whether w should buy (fast ma > slow ma)
def get_signal(fast, slow):
  print(f"\nFast {fast[-1]} \nSlow: {slow[-1]}")
  return fast[-1] > slow[-1]

# Get up-to-date 1 minute data from alpaca and add the moving averages
def get_sma_bars(ticker: str, exchange: str = 'CBSE'):
  bars = apca.get_bars_by_exchange(ticker=ticker, exchange=exchange)
  bars[f'sma_fast'] = get_sma(bars.close, SMA_FAST)
  bars[f'sma_slow'] = get_sma(bars.close, SMA_SLOW)
  print(f'\n-----\n{bars}\n-----\n')
  return bars

def sma_trade(ticker: str):
  while True:
    # get data
    bars = get_sma_bars(ticker=ticker)

    # check positions
    position = apca.get_all_positions(filter=ticker)
    should_buy = get_signal(bars.sma_fast, bars.sma_slow)
    print(f"\nPosition: {position} \nShould Buy: {should_buy}")

    # make decison to buy or sell based on provided information
    apca.make_trade_decision(ticker=ticker, position=position, decision=should_buy)

    time.sleep(get_pause())
    print("*"*20)


if __name__ == "__main__":
  #get_pause()
  #get_sma_bars(ticker='BTCUSD')
  sma_trade(ticker='BTCUSD')