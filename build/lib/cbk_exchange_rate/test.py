import requests
from bs4 import BeautifulSoup

url = "https://www.centralbank.go.ke/forex/"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

table = soup.find('table')
rows = table.find_all('tr')

for row in rows:
    cols = row.find_all('td')
    if cols and 'USD' in cols[0].text:
        print("USD Buying:", cols[1].text)
        print("USD Selling:", cols[2].text)
