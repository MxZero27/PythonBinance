from binance.client import Client
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

plt.style.use('ggplot')
# need to import API key
api_key = '*'
api_secret = '*'



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

def getmindata(symbol, interval, loopback,):
    frame = pd.DataFrame(client.get_historical_klines(symbol, interval, loopback + ' ago UTC'))
    # now we need to organize the frame. heres getting the first 6
    frame = frame.iloc[:, :6]
    # naming columns  'time','open','high','low','close','volume'
    frame.columns = ['Time', 'open', 'high', 'low', 'close', 'volume']
    frame = frame.set_index('Time')
    # timestamps are all in UNIX time. which counts seconds away from 1970.. nobody can read that.
    frame.index = pd.to_datetime(frame.index, unit='ms' )
    # all numbers that are being pulled are strings. Converting to FLOAT
    frame = frame.astype(float)
    return frame



testing = getmindata('DOGEUSDT', '1m', '1440m', )
print(testing)


# get avrg of our dataset.
print("High avg IS" + str(testing.high.mean()))
print("Low avg IS" + str(testing.low.mean()))
print("Open avg IS" + str(testing.open.mean()))
print("Close avg IS" + str(testing.close.mean()))

def animate(i):
    data = getmindata('BTCUSDT', '1m', '2880m')
    # clear access because there could be a price curve for every loop
    # get time and open price
    plt.plot(data.index, data.open, color='red')

    #sma 50
    data['MA 1'] = data['close'].rolling(window=50).mean()
    #sma 200
    data['MA 2'] = data['close'].rolling(window=200).mean()

    plt.plot(data['MA 1'], label='MA1', color='blue')
    plt.plot(data['MA 2'], label='MA2', color='green')
    # set labels & layout
    plt.xlabel('Time')
    plt.ylabel('Open Price')
    plt.tight_layout()

ani = FuncAnimation(plt.gcf(), animate, 1000)
plt.tight_layout()
plt.show()


