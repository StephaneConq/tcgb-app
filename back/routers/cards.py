from fastapi import APIRouter, Depends, File, UploadFile
from controllers.cards_controller import find_card_in_firestore, generate
from controllers.collection_controller import check_if_card_is_owned
from services.auth import get_current_user_email
from services.firestore import FirestoreService

router = APIRouter()

@router.post('/read')
async def read_cards(image: UploadFile = File(...), email: str = Depends(get_current_user_email)):
    """
    Route to receive a photo to read cards from
    """
    cards_read = generate(image)
    firestore_service = FirestoreService()
    cache_series = {}
    
    current_collection = firestore_service.query_documents(
        "collections",
        filters=[
            ("email", "==", email)
        ]
    )
    
    # Pre-process all cards at once to normalize data
    for card in cards_read:
        try:
            # cast to int and back to string to remove any leading zeros
            card['card_number'] = str(int(card.get("card_number", "0")))
        except ValueError:
            pass
        card['set_id'] = card.get('set_id', '').upper()
    
    # Batch process cards to reduce Firestore calls
    # Create a lookup dictionary to avoid redundant queries
    card_lookup = {}
    for card in cards_read:
        key = f"{card['set_id']}_{card['card_number']}"
        if key not in card_lookup:
            card_lookup[key] = {
                'card_number': card['card_number'],
                'set_id': card['set_id'],
                'licence': card.get('licence')
            }
    
    # Process unique cards and update cache
    for key, card_info in card_lookup.items():
        cards_data, cache_series = find_card_in_firestore(
            card_number=card_info['card_number'], 
            set_id=card_info['set_id'],
            firestore_service=firestore_service,
            cache_series=cache_series
        )
        card_lookup[key]['card_versions'] = cards_data
    
    # Apply results back to original cards
    for card in cards_read:
        key = f"{card['set_id']}_{card['card_number']}"
        card_data = card_lookup[key]['card_versions']
        card['card_versions'] = [
            {
                **c, 
                'ref': c.get('ref').path, 
                'licence': card.get('licence'),
                'count': check_if_card_is_owned(c.get('ref'), current_collection)
            } for c in card_data
        ]
            
    return {
        "cards": cards_read
    }

    
@router.get('')
async def get_card(card_number: str, set_id: str):
    """
    Get a card by its set id and card number
    """
    res, _ = find_card_in_firestore(card_number=card_number, set_id=set_id)
    if 'ref' in res:
        del res['ref']
    return {
        "card": res
    }