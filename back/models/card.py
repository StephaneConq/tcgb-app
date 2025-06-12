from typing import List, Optional
from pydantic import BaseModel


class Card(BaseModel):
    licence: str
    card_number: str
    set_id: str
    card_name: Optional[str]

class Cards(BaseModel):
    cards: List[Card]