from binance.client import Client
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import math

# need to import API key
#api_key = '**'
#api_secret = '**'
api_key = '4CiItbH07CfKO91417tke8vS9d1kLKbYxlXfUPQsCNVZHJ5v9bPF6OQLA79u5xTE'
api_secret = 'MOlIjUsuWq5IsABa5WPmw4yfUnKGSf294OYoflaFfOwtgsy96YKc6CXE7pzG4hXC'


# need to Connect Client
client = Client(api_key, api_secret, tld='us')


# define coin, interval, and time back. we will be getting bitcoin to usd every 1m for 30 m

# response = client.get_historical_klines('BTCUSDT','1m', '30m ago UTC')
# pd.DataFrame(client.get_historical_klines('BTCUSDT','1m', '30m ago UTC'))

### when outputting from pandas heres what we get: ###
#    "0",      // Open time
#    "1",      // Open
#    "2",      // High
#    "3",      // Low
#    "4",      // Close
#    "5",      // Volume
#    "6",      // Close time
#    "7",      // Quote asset volume
#    "8",      // Number of trades
#    "9",      // Taker buy base asset volume
#    "10",     // Taker buy quote asset volume
#    "11",     // Ignore.

# we dont need anything past volume.

def getmindata(symbol, interval, loopback):
    frame = pd.DataFrame(client.get_historical_klines(symbol, interval, loopback + ' ago UTC'))
    # now we need to organize the frame. heres getting the first 6
    frame = frame.iloc[:, :6]
    # naming columns  'time','open','high','low','close','volume'
    frame.columns = ['Time', 'open', 'high', 'low', 'close', 'volume']
    frame = frame.set_index('Time')
    # timestamps are all in UNIX time. which counts seconds away from 1970.. nobody can read that.
    frame.index = pd.to_datetime(frame.index, format='%Y%m%d', errors='ignore')
    # all numbers that are being pulled are strings. Converting to FLOAT
    frame = frame.astype(float)
    phigh = frame.high.mean()
    plow = frame.low.mean()
    popen = frame.open.mean()
    pclose = frame.close.mean()

    print("High avg IS" + str(phigh))
    print("Low avg IS" + str(plow))
    print("Open avg IS" + str(popen))
    print("Close avg IS" + str(pclose))
    return frame


testing = getmindata('DOGEUSDT', '1m', '1440m', )
print(testing)
plt.gcf().autofmt_xdate()
testing.plot(kind='hist',x='close',y='Time',color='red')


plt.tight_layout()
plt.show()
print(testing)

##this strat will buy if the asset falls more then .2% within the last 30 mins
# selling if asset rises by more then 0.15% this is where youd make money from trading fees. or falls further then 0.15%

def strategytest(symbol, qty, entry=False):
    df = getmindata(symbol, '1m', '30m', )
    attack = (df.Open.pct_change() + 1).cumprod() - 1
    if not entry:
        if attack[-1] < -0.002:
            order = client.create_order(symbol=symbol, side='BUY', type='MARKET', quantity=qty)
            print(order)

# print(response)