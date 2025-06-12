from datetime import datetime
from functions_framework import http
import requests
from services.firestore import FirestoreService


def process_cards(cards, headers):
    set_mapping = {}

    useful_headers = {
        "card_number": headers.index('id_normal'),
        "set_id": headers.index('set'),
        "card_name": headers.index('name'),
        "img_index": headers.index('id')
    }

    for card in cards:
        card_obj = {
            "card_number": card[useful_headers['card_number']],
            "set_id": card[useful_headers['set_id']],
            "card_name": card[useful_headers['card_name']],
            "card_img": f"https://static.dotgg.gg/onepiece/card/{card[useful_headers['img_index']]}.webp"
        }

        if card_obj.get('set_id') not in set_mapping:
            set_mapping[card_obj.get('set_id')] = []

        set_mapping[card_obj.get('set_id')].append(card_obj)

    return set_mapping


@http
def main(request):

    firestore_service = FirestoreService()

    r = requests.get('https://api.dotgg.gg/cgfw/getsets?game=one piece')
    sets = r.json()

    r = requests.get(
        'https://api.dotgg.gg/cgfw/getcards?game=onepiece&mode=indexed')
    cards_response = r.json()

    all_cards = process_cards(cards=cards_response.get(
        'data'), headers=cards_response.get('names'))

    for card_set in sets:
        existing_serie = firestore_service.query_documents(
            'series',
            filters=[
                ("set_id", "==", card_set.get('code'))
            ]
        )

        if not existing_serie:
            print(f"need to create {card_set.get('code')}")
            created_serie_id = firestore_service.create_document(
                "series",
                {
                    "date": datetime.fromtimestamp(float(card_set.get('ReleaseDate'))),
                    "licence": "one piece",
                    "serie_logo": f"https://static.dotgg.gg/onepiece/set-logo/{card_set.get('code')}.webp",
                    "serie_name": card_set.get('name'),
                    "set_id": card_set.get('code'),
                    "symbol_img": ""
                }
            )
            if created_serie_id:
                print(f"created {card_set.get('code')}")
                print(f"document id: {created_serie_id}")
                firestore_service.batch_create_sub_collection_documents(
                    "series",
                    created_serie_id,
                    "cards",
                    all_cards[card_set.get('code')]
                )
                print(f"created {len(all_cards[card_set.get('code')])} cards")
        else:
            print(f"{card_set.get('code')} already exists, skipping")

    return {"status": "ok"}
