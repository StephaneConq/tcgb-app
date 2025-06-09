

from concurrent.futures import ThreadPoolExecutor
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

def fetch_cards(series_id, user_email):
    
    firestore_service = FirestoreService()
    
    # Fetch collection cards
    collection_cards = firestore_service.query_sub_collection(
        "series",
        series_id,
        "cards"
    )
    
    # Extract card references once
    card_refs = [c.get('ref') for c in collection_cards]
    
    # Process in batches of 30 (Firestore limit for 'in' queries)
    # Use ThreadPoolExecutor for parallel batch processing
    user_cards = []
    
    def fetch_batch(batch):
        return firestore_service.query_sub_collection(
            "collections",
            user_email,
            "cards",
            filters=[("card_ref", "in", batch)]
        )
    
    batches = [card_refs[i:i+30] for i in range(0, len(card_refs), 30)]
    
    with ThreadPoolExecutor(max_workers=min(10, len(batches))) as executor:
        batch_results = list(executor.map(fetch_batch, batches))
    
    # Flatten results
    for batch in batch_results:
        user_cards.extend(batch)
    
    # Create a dictionary for O(1) lookup with path as key
    user_card_refs = {
        card.get('card_ref').path: card.get('count') for card in user_cards
    }
    
    # Pre-compute card numbers as integers to avoid repeated conversion
    card_numbers = {card.get('ref').path: int(card.get('card_number')) for card in collection_cards}
    
    # Process all cards at once with optimized lookup
    result = [
        {
            "card_name": card.get('card_name'),
            "set_id": card.get('set_id'),
            "card_number": card.get('card_number'),
            "card_img": card.get('card_img'),
            "_id": card.get('_id'),
            "ref": card.get('ref').path,
            'int_number': card_numbers[card.get('ref').path],
            'count': user_card_refs.get(card.get('ref').path, 0)
        }
        for card in collection_cards
    ]
    
    # Sort the results
    result.sort(key=lambda k: k['int_number'])
    
    return result