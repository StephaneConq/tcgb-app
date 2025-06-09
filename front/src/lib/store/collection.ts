import api from "$lib/axios";
import type CardModel from "$lib/models/card";


export const saveCards = async (cards: CardModel[]) => {
    const response = await api.patch(`/api/collection`, {
        cards
    });

    return response.data;
}

export const removeCard = async (cardRef: string) => {
    const response = await api.delete(`/api/collection?card_ref=${cardRef}`);

    return response.data;
}