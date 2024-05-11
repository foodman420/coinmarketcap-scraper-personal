import requests
from bs4 import BeautifulSoup
import sqlite3


def fetch_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        print("Failed to retrieve data")
        return None


def parse_data(html):
    soup = BeautifulSoup(html, 'html.parser')
    data_list = soup.find_all('tr', class_='cmc-table-row')[:20]
    cryptocurrencies = []
    for item in data_list:
        name_cell = item.find('td', class_='cmc-table__cell--sort-by__name')
        price_cell = item.find('td', class_='cmc-table__cell--sort-by__price')
        market_cap_cell = item.find(
            'td', class_='cmc-table__cell--sort-by__market-cap')

        name = name_cell.get_text(strip=True) if name_cell else "Unknown Name"
        price = price_cell.get_text(
            strip=True) if price_cell else "Unknown Price"
        market_cap = market_cap_cell.get_text(
            strip=True) if market_cap_cell else "Unknown Market Cap"

        cryptocurrencies.append({
            'name': name,
            'price': price,
            'market_cap': market_cap
        })
    return cryptocurrencies


def save_to_database(data):
    # Connect to SQLite database or create it if it doesn't exist
    conn = sqlite3.connect('cryptocurrencies.db')
    cursor = conn.cursor()

    # Create the table if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS crypto_data (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT,
                        price TEXT,
                        market_cap TEXT
                      )''')

    # Insert the data into the table
    for crypto in data:
        cursor.execute("INSERT INTO crypto_data (name, price, market_cap) VALUES (?, ?, ?)",
                       (crypto['name'], crypto['price'], crypto['market_cap']))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()


def main():
    url = 'https://coinmarketcap.com/all/views/all/'
    html = fetch_data(url)
    if html:
        crypto_data = parse_data(html)
        save_to_database(crypto_data)
        print("Data successfully saved to database.")


if __name__ == '__main__':
    main()
