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
            # cast to int and back to string to remove any leading zeros
            card['card_number'] = int(card["card_number"])
            card['card_number'] = str(card['card_number'])
        except ValueError:
            pass
        
        card['set_id'] = card.get('set_id', '').upper()

        card_data = get_card_data(card["set_id"], card["card_number"])
        card["card_img"] = card_data["image"]
        card["variants"] = card_data["variants"]
    return {
        "cards": cards_read
    }
    
@router.get('')
async def get_card(card_number: str, set_id: str):
    """
    Get a card by its set id and card number
    """
    card = {
        "card_number": card_number,
        "set_id": set_id
    }
    
    card_data = get_card_data(card["set_id"], card["card_number"])
    card["card_img"] = card_data["image"]
    card["variants"] = card_data["variants"]
    return {
        "card": card
    }