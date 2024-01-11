import requests
import pandas as pd
from datetime import datetime
from config import apikey

date = '2024-01-09'
apikey = apikey

# Get data
url = f'https://api.polygon.io/v2/aggs/ticker/AAPL/range/1/second/{date}/{date}?adjusted=true&sort=asc&limit=50000&apiKey={apikey}'
response = requests.get(url).json()
results = response.get('results', [])
data = pd.DataFrame(results)

# Data prep
data['consistency'] = data['t'] - data['t'].shift(1)
data['date'] = data['t'].apply(lambda x: datetime.fromtimestamp(x / 1000))

# Save
data.to_csv(f'data/{date}.csv', index=False)