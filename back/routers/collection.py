from fastapi import APIRouter
from controllers.collection_controller import update_cards_in_collection

router = APIRouter()

@router.patch('')
async def update_collection(body: dict):
    """
    Route to update a document in a collection
    """
    return {
        "response": update_cards_in_collection(body.get('cards'))
    }
    