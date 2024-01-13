import requests
import pandas as pd
from datetime import datetime
from config import apikey

date = '2024-01-09'
ticker = 'AAPL'
apikey = apikey

# Get data
url = f'https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/second/{date}/{date}?adjusted=true&sort=asc&limit=50000&apiKey={apikey}'
response = requests.get(url).json()
results = response.get('results', [])
data = pd.DataFrame(results)

# Data prep
data['simpletime'] = data.index + 1
data['date'] = data['t'].apply(lambda x: datetime.fromtimestamp(x / 1000))
data['vwap'] = (data['vw'] * data['v']).cumsum() / data['v'].cumsum()
data = data.rename(columns={'v': 'volume', 'o': 'open', 'c': 'close', 'h': 'high', 'l': 'low', 'n': 'num_trades'})

# Save
data.to_csv(f'data/{ticker} {date}.csv', index=False)