import re
from bs4 import BeautifulSoup
import logging
import requests

def get_card_data(set: str, number: str) -> dict:
    """
    Get the data for a card from the Limitless TCG website
    """
    try:
        number = int(number)
    except ValueError:
        logging.warning(f'Invalid number: {number}')

    url = f"https://limitlesstcg.com/cards/jp/{set}/{number}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    card_data = {}
    card_data["image"] = soup.find("img", {"class": "card"})["src"]
    
    # Find the table with card variants
    table = soup.find("table", {"class": "card-prints-versions"})
    
    variants = []
    if table:
        # Process each row in the table
        for row in table.find_all("tr"):
            # Skip header rows
            if row.find("th"):
                continue
                
            # Find the card number
            card_number_span = row.find("span", {"class": "prints-table-card-number"})
            if card_number_span:
                card_number = card_number_span.text.strip("#")
                
                # Find the USD price link if it exists
                price_link = row.find("a", {"class": "card-price usd"})
                if price_link and 'href' in price_link.attrs:
                    href = price_link['href']
                    # Extract product ID
                    match = re.search(r'product%2F(\d+)', href)
                    if match:
                        product_id = match.group(1)
                        variants.append({
                            "number": card_number,
                            "product_id": product_id
                        })
    
    card_data["variants"] = variants
    return card_data
