

from services.firestore import FirestoreService


def get_all_sets(licence: str = None):
    """
    Get all Pokemon TCG sets
    """
    firestore_service = FirestoreService()
    filters = []
    if licence:
        filters.append(
            ("licence", "==", licence)
        )
    sets = firestore_service.query_documents('series', order_by='date', filters=filters, direction="DESCENDING")
    return sets

def get_cards_in_set(set_doc_id: str):
    """
    Get cards by Firestore doc set id
    """
    firestore_service = FirestoreService()
    cards = firestore_service.query_sub_collection(
        collection_name='series',
        document_id=set_doc_id,
        sub_collection='cards'
    )
    for card in cards:
        try:
            card['int_number'] = int(card['card_number'])
        except KeyError:
            pass
    return sorted(cards, key=lambda k: k['int_number'])
