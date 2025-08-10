from fastapi import APIRouter, Depends, Body
from controllers.collection_controller import update_cards_in_collection, delete_card_from_collection
from services.auth import get_current_user_email

router = APIRouter()

@router.patch('')
async def update_collection(body: dict = Body(...), email: str = Depends(get_current_user_email)):
    """
    Route to update a document in a collection
    """
    return {
        "response": update_cards_in_collection(body.get('cards'), email)
    }
    
@router.delete('')
async def delete(card_ref: str, email: str = Depends(get_current_user_email)):
    """
    Route to remove a card from the collection
    """
    return {
        "response": delete_card_from_collection(card_ref, email)
    }