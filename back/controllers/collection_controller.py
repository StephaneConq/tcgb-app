from typing import List

from fastapi import HTTPException
from services.firestore import FirestoreService


def update_cards_in_collection(cards: List[dict], email: str, licence: str):
    """
    Controller function to update a document in a collection
    """
    firestore_service = FirestoreService()
    series = {
        
    }

    for card in cards:
        
        card['card_number'] = card.get('card_number').upper()
        card['set_id'] = card.get('set_id').upper()
        
        if card.get('set_id') not in series:
            serie_doc = firestore_service.query_documents(
                collection_name='series',
                filters=[
                    ('set_id', '==', card['set_id'])
                ]
            )
            series_card = firestore_service.query_sub_collection(
                collection_name='series',
                document_id=serie_doc[0].get('_id'),
                sub_collection='cards',
            )
            series[card['set_id']] = {
                'id': serie_doc[0].get('_id'),
                'cards': series_card
            }
        
        card_refs_in_serie = [c.get('ref') for c in series[card['set_id']]['cards'] if c.get('card_number') == card['card_number']]
        
        if len(card_refs_in_serie) > 0:
            card_found = firestore_service.query_sub_collection(
                collection_name='collections',
                document_id=email,
                sub_collection="cards",
                filters=[
                    ('card_ref', '==', card_refs_in_serie[0])
                ]
            )
        
        if len(card_found) > 0:
            firestore_service.update_sub_collection_document(
                collection_name='collections',
                document_id=email,
                sub_collection="cards",
                sub_document_id=card_found[0].get('_id'),
                data={
                    'count': card_found[0].get('count') + 1 if card_found[0].get('count') else 1
                }
            )
        else:
            firestore_service.create_sub_collection_document(
                collection_name='collections',
                document_id=email,
                sub_collection='cards',
                data={
                    'card_ref': card_refs_in_serie[0],
                    'count': 1,
                    'licence': licence
                }
            )
    
    return True


def delete_card_from_collection(card_path: str, email: str):
    """
    Remove a card from a user's collection
    """
    firestore_service = FirestoreService()
    
    card_ref = firestore_service.get_document_ref_by_path(card_path)
    
    if not card_ref:
        raise HTTPException(status_code=404, detail=f"Card with path {card_path} not found")
    
    user_card = firestore_service.query_sub_collection(
        "collections",
        email,
        "cards",
        filters=[
            ('card_ref', '==', card_ref)
        ]
    )
    
    if len(user_card):
        user_card = user_card[0]
        new_count = user_card.get('count', 0) - 1
        
        if new_count > 0:
            firestore_service.update_sub_collection_document(
                "collections",
                email,
                "cards",
                user_card.get('_id'),
                {
                    'count': new_count
                }
            )
        else:
            if new_count < 0:
                raise HTTPException(status_code=400, detail="Cannot remove more cards than available")
            
            firestore_service.delete_sub_collection_document(
                "collections",
                email,
                "cards",
                user_card.get('_id')
            )
        
        return True
    else:
        raise HTTPException(status_code=404, detail=f"Card with path {card_path} not found")
