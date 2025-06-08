import api from "$lib/axios";
import type CardModel from "$lib/models/card";


export const saveCards = async (cards: Card[]) => {
    const response = await api.patch(`/api/collection`, {
        cards
    });

    return response.data;
}