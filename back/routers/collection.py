from fastapi import APIRouter, Depends
from controllers.collection_controller import update_cards_in_collection
from services.auth import get_current_user_email

router = APIRouter()

@router.patch('')
async def update_collection(body: dict, email: str = Depends(get_current_user_email)):
    """
    Route to update a document in a collection
    """
    return {
        "response": update_cards_in_collection(body.get('cards'), email)
    }
    