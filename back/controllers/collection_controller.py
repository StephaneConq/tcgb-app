from typing import List
from services.firestore import FirestoreService


def update_cards_in_collection(cards: List[dict], email: str, licence: str):
    """
    Controller function to update a document in a collection
    """
    firestore_service = FirestoreService()

    for card in cards:
        card_found = firestore_service.query_sub_collection(
            collection_name='collections',
            document_id=email,
            sub_collection="cards",
            filters=[
                ('set_tag', '==', card['set_tag']),
                ('card_number', '==', card['card_number'])
            ]
        )
        
        if card_found:
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
            try:
                del card['selected']
            except KeyError:
                pass
            
            card['count'] = 1
            card['licence'] = licence
            firestore_service.create_sub_collection_document(
                collection_name='collections',
                document_id=email,
                sub_collection='cards',
                data=card
            )
    
    return True