from fastapi import APIRouter

from fastapi import APIRouter
from controllers.sets_controller import get_all_sets, get_cards_in_set

router = APIRouter()

@router.get('')
async def get_sets(licence: str = None):
    return {
        "series": get_all_sets(licence)
    }

@router.get('/{serie_doc_id}/cards')
async def get_cards(serie_doc_id: str):
    return {
        "cards": get_cards_in_set(serie_doc_id)
    }