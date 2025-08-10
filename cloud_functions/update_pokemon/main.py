import os
import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from services.firestore import FirestoreService
from functions_framework import http

from services.helpers import extract_product_id


def get_all_sets_pokemon():
    """
    Get all Pokemon TCG sets
    """
    r = requests.get('https://www.pokecardex.com/series/jp')
    soup = BeautifulSoup(r.text, 'html.parser')
    series_soup = soup.find_all('div', {'class': 'serie-container'})
    series = []
    for serie_soup in series_soup:
        symbol = serie_soup.find('img', {'class': 'symbole-jp'})
        symbol_img = symbol.get('src')
        serie_name = symbol.get('alt')

        if symbol_img:
            # Extract the filename without extension from the URL
            filename = os.path.basename(symbol_img)
            # Remove the file extension
            set_id = os.path.splitext(filename)[0]
        else:
            set_id = None

        serie_logo = serie_soup.find(
            'img', {'class': 'serie-logo-jp'}).get('src')
        # Add to series list
        series.append({
            'set_id': set_id,
            'symbol_img': symbol_img,
            'serie_name': serie_name,
            'serie_logo': serie_logo,
            'licence': 'pokemon'
        })

    return series


def get_cards(serie):
    """
    Get all cards from a serie
    """
    r = requests.get(
        f"https://www.pokecardex.com/series/jp/{serie.get('set_id')}")
    soup = BeautifulSoup(r.text, 'html.parser')
    date = soup.find('div',
                     {
                         'class': 'd-flex align-items-center d-none d-lg-block justify-content-lg-start'
                     }
                     )
    if date:
        date_text = date.text.strip()
        try:
            # Assuming the date format is something like "DD Month YYYY"
            # Adjust the format string to match your actual date format
            parsed_date = datetime.strptime(date_text, "%d/%m/%Y")
            # Firestore will convert this to a timestamp
            serie['date'] = parsed_date
        except ValueError:
            # Fallback if parsing fails
            serie['date'] = date_text

    cards_soup = soup.find_all('img', {'class': 'img-fluid br-10 dark-shadow'})
    cards = []

    for card_soup in cards_soup:

        if card_soup.get('src'):
            # Extract the filename without extension from the URL
            filename = os.path.basename(card_soup.get('src'))
            # Remove the file extension
            card_number = os.path.splitext(filename)[0]
        else:
            card_number = None
        cards.append({
            'card_name': card_soup.get('alt'),
            'card_img': card_soup.get('src'),
            'card_number': card_number,
            'set_id': serie.get('set_id')
        })
    return serie, cards


@http
def main(request):
    firestore_service = FirestoreService()
    series = get_all_sets_pokemon()

    for i, serie in enumerate(series):
        print(f"{i + 1}/{len(series)}: {serie.get(('serie_name'))}")
        existing_serie = firestore_service.query_documents(
            "series",
            filters=[
                ('set_id', '==', serie.get('set_id')),
                ('licence', '==', serie.get('licence'))
            ]
        )

        if not existing_serie:
            serie, cards = get_cards(serie)

            print('serie does not exist, creating')
            created_serie_id = firestore_service.create_document(
                "series", serie)
            print(f"Serie created: {created_serie_id}")

            if created_serie_id:

                firestore_service.batch_create_sub_collection_documents(
                    "series",
                    created_serie_id,
                    "cards",
                    cards
                )
                print(f"Cards created: {len(cards)}")
        print(f"{i + 1}/{len(series)}: {serie} done")

    return "Series created"


@http
def update_prices(request=None):
    firestore_service = FirestoreService()
    sets = firestore_service.query_documents('series')

    for set in sets:
        cards = firestore_service.query_sub_collection(
            'series',
            set.get('_id'),
            'cards'
        )

        for card in cards:
            r = requests.post(f"https://mp-search-api.tcgplayer.com/v1/search/request?q={card.get('set_id')}+{sanitize_card_name(card.get('card_name'))}+{card.get('card_number')}&isList=false&mpfev=3857",
                              data={
                "algorithm": "sales_dismax",
                "from": 0,
                "size": 24,
                "filters": {
                    "term": {},
                    "range": {},
                    "match": {}
                },
                "listingSearch": {
                    "context": {
                        "cart": {}
                    },
                    "filters": {
                        "term": {
                            "sellerStatus": "Live",
                            "channelId": 0
                        },
                        "range": {
                            "quantity": {
                                "gte": 1
                            }
                        },
                        "exclude": {
                            "channelExclusion": 0
                        }
                    }
                },
                "context": {
                    "cart": {},
                    "shippingCountry": "FR",
                    "userProfile": {}
                },
                "settings": {
                    "useFuzzySearch": True,
                    "didYouMean": {}
                },
                "sort": {}
            })
            res = r.json()
            print(res)
            pass


def sanitize_card_name(name):
    return name.replace('—', '').strip()

update_prices()
