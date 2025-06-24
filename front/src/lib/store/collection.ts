import api from "$lib/axios";
import type CardModel from "$lib/models/card";

export const saveCards = async (cards: CardModel[]) => {
    // Create a sanitized version of the cards without circular references
    const sanitizedCards = cards.map(card => {
        // Only include the necessary properties for the API
        return {
            _id: card._id,
            ref: card.ref,
            set_id: card.set_id,
            card_number: card.card_number,
            count: card.count
            // Add any other properties needed by your API
        };
    });

    const response = await api.patch(`/api/collection`, {
        cards: sanitizedCards
    });

    return response.data;
}

export const removeCard = async (cardRef: string) => {
    const response = await api.delete(`/api/collection?card_ref=${cardRef}`);

    return response.data;
}
