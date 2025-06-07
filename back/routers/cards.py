from fastapi import APIRouter, File, UploadFile
from controllers.cards_controller import generate
from controllers.limitless_tcg_controller import get_card_data

router = APIRouter()

@router.post('/read')
async def read_cards(image: UploadFile = File(...)):
    """
    Route to receive a photo to read cards from
    """
    cards_read = generate(image)
    for card in cards_read:
        
        try:
            card['card_number'] = int(card["card_number"])
            card['card_number'] = str(card['card_number'])
        except ValueError:
            pass
        
        card_data = get_card_data(card["set_tag"], card["card_number"])
        card["image"] = card_data["image"]
        card["variants"] = card_data["variants"]
    return {
        "cards": cards_read
    }