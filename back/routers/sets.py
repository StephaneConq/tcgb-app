from fastapi import APIRouter, Depends

from fastapi import APIRouter
from controllers.sets_controller import get_all_sets, fetch_cards
from services.auth import get_current_user_email

router = APIRouter()

@router.get('')
async def get_sets(licence: str = None):
    return {
        "series": get_all_sets(licence)
    }

@router.get('/{serie_doc_id}/cards')
async def get_cards(serie_doc_id: str, email: str = Depends(get_current_user_email)):
    return {
        "cards": fetch_cards(serie_doc_id, email) 
    }