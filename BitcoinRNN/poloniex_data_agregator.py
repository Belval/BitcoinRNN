import os
import requests

# TODO: Multithread this

# Period for which we want the data, here 14400 is 4 hours
# Available period are: 300, 900, 1800, 7200, 14400, and 86400
period = '1800'

# The Poloniex API address
r = requests.get('https://poloniex.com/public?command=returnChartData&currencyPair=USDT_BTC&start=1420070400&end=1483228800&period={}'.format(period))
# The file where we write our data 
f = open('data/polo_{}.dat'.format(period), 'w')
# The text that will be written to the file
text = ''
# The length of the data we have
dataLen = len(r.json()) - 1
# We extract what is considered "valuable data"
# High | Low | High - Low | High - PreviousHigh | Low - PreviousLow | Open | Close | Open - Close | Volume | QuoteVolume | WeightedAverage | WeightedAverage - PreviousWeightedAverage | WeightedAverage - 5 days average | WeightedAverage - 10 days average
# We extract the true or false (1 or 0) value which is CurrentWeightedAverage < NextWeightedAverage meaning, did the value increase
# Exemple: {'date': 1483012800, 'high': 979.4, 'low': 964, 'open': 977.0000009, 'close': 964, 'volume': 167546.54720738, 'quoteVolume': 172.67076146, 'weightedAverage': 970.32378725}
for val in range(11, dataLen):
    # The value
    obj = r.json()[val]
    # The previous 10
    prev10Obj = r.json()[val - 10:val]
    # The previous 5
    prev5Obj = prev10Obj[5:]
    # The previous value
    prevObj = r.json()[val - 1]
    # The next value
    nextObj = r.json()[val + 1]
    # Formatting of the line
    text = text + '{:.4f},{:.4f},{:.4f},{:.4f},{:.4f},{:.4f},{:.4f},{:.4f},{:.4f},{:.4f},{:.4f},{:.4f},{:.4f},{:.4f},{}\n' \
    .format(
        obj['high'],
        obj['low'], 
        obj['high'] - obj['low'], 
        obj['high'] - prevObj['high'], 
        obj['low'] - prevObj['low'], 
        obj['open'], 
        obj['close'], 
        obj['open'] - obj['close'], 
        obj['volume'], 
        obj['quoteVolume'], 
        obj['weightedAverage'], 
        obj['weightedAverage'] - prevObj['weightedAverage'], 
        obj['weightedAverage'] - sum(c['weightedAverage'] for c in prev5Obj) / 5, 
        obj['weightedAverage'] - sum(c['weightedAverage'] for c in prev10Obj) / 10, 
        obj['weightedAverage'])
    # Output to see where we are in the process
    if val % 100 == 0:
        print(str(val) + ' / ' + str(dataLen))

# Write the text to the file. It would be interesting to benchmark if it's faster to write each line instead of one big string.
f.write(text)
# Close the file
f.close()
