from bs4 import BeautifulSoup
import requests
import pandas as pd

url = "http://openinsider.com/search?q=AAPL"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Find the table
table = soup.find('table', class_='tinytable')

# Extract table rows
rows = table.find_all('tr')

# Create an empty list to store the data
data = []

# Loop through rows and extract data
for row in rows:
    cells = row.find_all('td')
    if cells:
        insider_info = {
            'X': cells[0].get_text(strip=True),
            'Filing Date': cells[1].get_text(strip=True),
            'Trade Date': cells[2].get_text(strip=True),
            'Ticker': cells[3].get_text(strip=True),
            'Insider Name': cells[4].get_text(strip=True),
            'Title': cells[5].get_text(strip=True),
            'Trade Type': cells[6].get_text(strip=True),
            'Price': cells[7].get_text(strip=True),
            'Qty': cells[8].get_text(strip=True),
            'Owned': cells[9].get_text(strip=True),
            'ΔOwn': cells[10].get_text(strip=True),
            'Value': cells[11].get_text(strip=True)
        }
        data.append(insider_info)

# Convert the list of dictionaries to a DataFrame
df = pd.DataFrame(data)

# Save DataFrame to CSV
df.to_csv('insider_trades.csv', index=False)
