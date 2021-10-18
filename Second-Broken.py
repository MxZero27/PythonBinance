from binance.client import Client
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import math

# need to import API key
api_key = '**'
api_secret = '**'



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

# Get data and put it in a frame.
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
		
		#calculating the avg of a column 
    phigh = frame.high.mean()
    plow = frame.low.mean()
    popen = frame.open.mean()
    pclose = frame.close.mean()
		
		#print and wrap the float into a string
    print("High avg IS" + str(phigh))
    print("Low avg IS" + str(plow))
    print("Open avg IS" + str(popen))
    print("Close avg IS" + str(pclose))
    return frame

#this works
testing = getmindata('DOGEUSDT', '1m', '1440m', )
print(testing)

#this doesnt
testing.plot(kind='hist',x='close',y='Time',color='red')
plt.gcf().autofmt_xdate()
plt.tight_layout()
plt.show()
