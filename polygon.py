import requests

apikey = 'ri7JaTcMgVHQB8du8WJHGQj6IYDTagNW'
url = f'https://api.polygon.io/v2/aggs/ticker/AAPL/range/1/second/2023-01-09/2023-01-09?apiKey={apikey}'

response = requests.get(url).json()

print(response)