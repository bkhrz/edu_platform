import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from urllib.parse import urljoin


def scrape_transport_data():
    """scrape transport listings from OLX.uz - single page only"""

    base_url = "https://www.olx.uz"
    transport_url = "https://www.olx.uz/transport/"

    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    })

    scraped_data = []

    print("Scraping transport data from OLX.uz ...")

    try:
        # Get page content
        response = session.get(transport_url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # Save HTML for debugging
        with open('page_source.html', 'w', encoding='utf-8') as f:
            f.write(soup.prettify())


        selectors_to_try = [
            'div[data-cy="l-card"]'
        ]

        listings = []
        used_selector = None

        for selector in selectors_to_try:
            listings = soup.select(selector)
            if listings:
                used_selector = selector
                break

        if not listings:
            print("No listings found with standard selectors.")
            return

        # Extract data from each listing
        for i, listing in enumerate(listings):
            data = {}

            try:
                # Extract title - try multiple approaches
                title = 'N/A'
                title_candidates = [
                    listing.find('h6'),
                    listing.find('h3'),
                    listing.find('h4'),
                    listing.find('a', href=True),
                    listing.find(attrs={'data-cy': 'ad-card-title'})
                ]

                for candidate in title_candidates:
                    if candidate and candidate.get_text(strip=True):
                        title = candidate.get_text(strip=True)
                        break

                data['title'] = title

                price = 'N/A'
                text_content = listing.get_text()

                # Look for various price patterns
                price_patterns = [
                    r'[\d\s,]+\s*\$',  # USD: 8800$, 1,500 $
                    r'\$\s*[\d\s,]+',  # USD: $ 8800, $ 1,500
                    r'[\d\s,]+\s*сўм',  # UZS: 150000 сўм
                    r'сўм\s*[\d\s,]+',  # UZS: сўм 150000
                    r'[\d\s,]+\s*руб',  # RUB: 50000 руб
                    r'[\d\s,]+\s*EUR',  # EUR: 7500 EUR
                    r'[\d\s,]+\s*€',  # EUR: 7500 €
                    r'[\d\s,]+\s*млн',  # Million: 5 млн
                    r'[\d\s,]+\s*тыс',  # Thousand: 150 тыс
                ]

                for pattern in price_patterns:
                    matches = re.findall(pattern, text_content, re.IGNORECASE)
                    if matches:
                        price = max(matches, key=len).strip()
                        break

                if price == 'N/A':
                    number_matches = re.findall(r'\b\d{4,}\b', text_content)
                    if number_matches:
                        potential_prices = [num for num in number_matches
                                            if not (2000 <= int(num) <= 2025) and int(num) >= 1000]
                        if potential_prices:
                            price = potential_prices[0]

                data['price'] = price

                # Extract location
                location = 'N/A'
                # Look for common Uzbek cities
                cities = ['Ташкент', 'Самарканд', 'Бухара', 'Наманган', 'Андижан',
                          'Фергана', 'Карши', 'Термез', 'Ургенч', 'Коканд']

                for city in cities:
                    if city in text_content:
                        location = city
                        break

                data['location'] = location
                data['date'] = 'N/A'  # Date extraction can be added later if needed

                # Extract link
                link = 'N/A'
                link_elem = listing.find('a', href=True)
                if link_elem:
                    href = link_elem.get('href')
                    if href:
                        if href.startswith('/'):
                            link = urljoin(base_url, href)
                        elif href.startswith('http'):
                            link = href

                data['link'] = link

                scraped_data.append(data)

            except Exception as e:
                print(f"Error extracting listing {i}: {e}")
                continue

    except requests.RequestException as e:
        print(f"Error fetching page: {e}")
        return

    # Save to CSV
    if scraped_data:
        df = pd.DataFrame(scraped_data)
        filename = 'transport_data.csv'
        df.to_csv(filename, index=False, encoding='utf-8')

        print(f"\nScraping completed!")
        print(f"Total transport listings scraped: {len(scraped_data)}")
        print(f"Data saved to: {filename}")

    else:
        print("No data was scraped!")


if __name__ == "__main__":
    scrape_transport_data()