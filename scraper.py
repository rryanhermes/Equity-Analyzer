import requests
from bs4 import BeautifulSoup
import base64
import json

# Helper function to decrypt payload using the key
def decrypt_payload(key, payload):
    data = base64.b64decode(payload)
    cipher = "".join([chr(data[i]) for i in range(0, len(data), 2)])
    decrypted_data = ""
    for i in range(0, len(cipher)):
        c_num = ord(cipher[i])
        k_num = ord(key[i % len(key)])
        c2 = c_num ^ k_num
        decrypted_data += chr(c2)
    return decrypted_data

url = "https://marketchameleon.com/Overview/ADBE/Earnings/Earnings-Dates"
session = requests.Session()

print("Sending request to URL...")
r = session.get(url)
print(f"Response status code: {r.status_code}")

if r.status_code != 200:
    raise ValueError("Failed to retrieve the webpage")

soup = BeautifulSoup(r.text, "html.parser")
print("Parsed HTML with BeautifulSoup")

# Define the decryption key
key = "97523022"

encryptedDivs = [i.get("cipherxx") for i in soup.find_all("div") if i.get("cipherxx")]
print(f"Found {len(encryptedDivs)} encrypted divs")

if not encryptedDivs:
    raise ValueError("No encrypted divs found with 'cipherxx' attribute.")

unencrypted = []
for index, div in enumerate(encryptedDivs):
    decrypted_data = decrypt_payload(key, div)
    unencrypted.append(decrypted_data)
    print(f"Decrypted div {index}: {decrypted_data[:100]}...")  # Print first 100 chars for brevity

# Assuming unencrypted[2] contains the second table as per your comment
if len(unencrypted) < 3:
    raise ValueError("Expected at least 3 decrypted divs, but got fewer.")

print("Parsing the third decrypted div for table data")
soup = BeautifulSoup(unencrypted[2], "html.parser")

tbody = soup.find("tbody")
if tbody:
    rows = tbody.findAll("tr", recursive=False)
    print(f"Found {len(rows)} rows in tbody")
else:
    raise ValueError("No tbody found in the decrypted HTML")

thead = soup.find("thead")
if thead:
    headers = thead.findAll("tr", recursive=False)
    print(f"Found {len(headers)} rows in thead")
else:
    print("No thead found in the decrypted HTML")

table2 = [
    {
        "Date": t[0].text.strip(),
        "Time": t[1].text.strip(),
        "Period": t[2].text.strip(),
        "Conference Call": t[3].text.strip(),
        "Price Effect": t[4].find("span").text if t[4].find("span") else t[4].text.strip(),
        "Implied Straddle": t[5].text.strip(),
        "Closing Price": t[6].text.strip(),
        "Opening Gap": t[7].text.strip(),
        "Drift Since": t[8].text.strip(),
        "Range Since": t[9].text.strip(),
        "Price Change 1 Week Before": t[10].text.strip(),
        "Price Change 1 Week After": t[11].text.strip()
    }
    for t in (t.findAll('td', recursive=False) for t in rows)
    if len(t) >= 11
]

print(json.dumps(table2, indent=4, sort_keys=True))
